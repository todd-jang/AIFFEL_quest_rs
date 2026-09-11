# ============================================================
# Korean Chatbot Transformer
# songys/chatbot_data.csv
# ============================================================

import os
import re
import random
import math
import pandas as pd
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ------------------------------------------------------------
# 1. Reproducibility
# ------------------------------------------------------------

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", device)


# ------------------------------------------------------------
# 2. Hyperparameters
# ------------------------------------------------------------

N_LAYERS = 1
D_MODEL = 368
N_HEADS = 8
D_FF = 1024
DROPOUT = 0.2

WARMUP_STEPS = 1000
BATCH_SIZE = 64
EPOCHS = 20

MAX_LEN = 40

PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"
BOS_TOKEN = "<start>"
EOS_TOKEN = "<end>"

SPECIAL_TOKENS = [
    PAD_TOKEN,
    UNK_TOKEN,
    BOS_TOKEN,
    EOS_TOKEN
]


# ------------------------------------------------------------
# 3. Load Dataset
# ------------------------------------------------------------

# songys/Chatbot_data 저장소의 원본 CSV를 스크립트 폴더에 저장
import urllib.request

DATA_URL = "https://raw.githubusercontent.com/songys/Chatbot_data/master/ChatbotData.csv"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "ChatbotData.csv")

if not os.path.exists(DATA_PATH):
    print("Downloading dataset from GitHub...")
    urllib.request.urlretrieve(DATA_URL, DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print(df.head())


# ------------------------------------------------------------
# 4. Column detection
# ------------------------------------------------------------

# songys/chatbot_data.csv는 일반적으로
# Q : 질문
# A : 답변
# label : 분류
#
# 컬럼명이 다른 경우 자동 대응

if "Q" in df.columns and "A" in df.columns:
    question_col = "Q"
    answer_col = "A"
elif "question" in df.columns and "answer" in df.columns:
    question_col = "question"
    answer_col = "answer"
else:
    question_col = df.columns[0]
    answer_col = df.columns[1]

print("Question column:", question_col)
print("Answer column:", answer_col)


# ------------------------------------------------------------
# 5. Text Cleaning
# ------------------------------------------------------------

def clean_text(text):
    text = str(text)

    # 한글, 영문, 숫자, 기본 문장부호만 유지
    text = re.sub(r"[^가-힣a-zA-Z0-9\s.,!?~]", " ", text)

    # 연속 공백 제거
    text = re.sub(r"\s+", " ", text)

    return text.strip()


df[question_col] = df[question_col].astype(str).apply(clean_text)
df[answer_col] = df[answer_col].astype(str).apply(clean_text)

# 빈 문장 제거
df = df[
    (df[question_col].str.len() > 0) &
    (df[answer_col].str.len() > 0)
].reset_index(drop=True)

print("Cleaned dataset:", len(df))


# ------------------------------------------------------------
# 6. Data Augmentation
# ------------------------------------------------------------

WORD2VEC_PATH = os.path.join(SCRIPT_DIR, "ko.bin")
word2vec_model = None

if os.path.exists(WORD2VEC_PATH):
    try:
        from gensim.models import KeyedVectors, Word2Vec
        from gensim.utils import SaveLoad

        try:
            word2vec_model = Word2Vec.load(WORD2VEC_PATH).wv
        except Exception:
            try:
                original_load_specials = Word2Vec._load_specials
                Word2Vec._load_specials = SaveLoad._load_specials
                try:
                    legacy_model = Word2Vec.load(WORD2VEC_PATH, mmap=None)
                finally:
                    Word2Vec._load_specials = original_load_specials

                word2vec_model = KeyedVectors(
                    vector_size=legacy_model.vector_size
                )
                word2vec_model.index_to_key = list(legacy_model.index2word)
                word2vec_model.key_to_index = {
                    word: index
                    for index, word in enumerate(word2vec_model.index_to_key)
                }
                word2vec_model.vectors = legacy_model.syn0
            except Exception:
                word2vec_model = KeyedVectors.load_word2vec_format(
                    WORD2VEC_PATH,
                    binary=True
                )
        print("Loaded Word2Vec:", WORD2VEC_PATH)
    except Exception as error:
        print("Word2Vec disabled:", error)
else:
    print("Word2Vec not found; using noise injection only:", WORD2VEC_PATH)


def lexicon_substitution(text, probability=0.25):
    if word2vec_model is None:
        return text

    words = text.split()
    substituted = []

    for word in words:
        lookup_word = word.strip(".,!?~")

        if (
            random.random() < probability and
            lookup_word in word2vec_model.key_to_index
        ):
            candidates = word2vec_model.most_similar(
                lookup_word,
                topn=10
            )
            candidates = [
                candidate
                for candidate, similarity in candidates
                if candidate != lookup_word and " " not in candidate
            ]

            if candidates:
                replacement = random.choice(candidates)
                suffix = word[len(lookup_word):]
                word = replacement + suffix

        substituted.append(word)

    return " ".join(substituted)


def noise_injection(text):
    words = text.split()
    if len(words) > 2:
        idx = random.randint(0, len(words) - 2)
        words[idx], words[idx+1] = words[idx+1], words[idx]
    return " ".join(words)

def augment_data(df, question_col, answer_col, target_size=30000):
    augmented_list = []
    current_size = len(df)
    
    while len(augmented_list) + current_size < target_size:
        idx = random.randint(0, current_size - 1)
        q = df.iloc[idx][question_col]
        a = df.iloc[idx][answer_col]
        
        # 유사어 치환 후 일부 샘플에 단어 순서 noise 적용
        aug_q = lexicon_substitution(q)
        if random.random() < 0.5:
            aug_q = noise_injection(aug_q)
        augmented_list.append({question_col: aug_q, answer_col: a})
        
    return pd.concat([df, pd.DataFrame(augmented_list)], ignore_index=True)

df = augment_data(df, question_col, answer_col)
print("Augmented dataset size:", len(df))


# ------------------------------------------------------------
# 7. Train / Validation Split
# ------------------------------------------------------------

indices = np.arange(len(df))
np.random.shuffle(indices)

split = int(len(indices) * 0.9)

train_indices = indices[:split]
valid_indices = indices[split:]

train_df = df.iloc[train_indices].reset_index(drop=True)
valid_df = df.iloc[valid_indices].reset_index(drop=True)

print("Train:", len(train_df))
print("Validation:", len(valid_df))


# ------------------------------------------------------------
# 8. Tokenizer
# ------------------------------------------------------------

def tokenize(text):
    # 간단한 한국어 whitespace tokenizer
    return text.split()


# ------------------------------------------------------------
# 9. Vocabulary
# ------------------------------------------------------------

counter = {}

for text in train_df[question_col]:
    for token in tokenize(text):
        counter[token] = counter.get(token, 0) + 1

for text in train_df[answer_col]:
    for token in tokenize(text):
        counter[token] = counter.get(token, 0) + 1


# 빈도순 정렬
tokens = sorted(
    counter.items(),
    key=lambda x: x[1],
    reverse=True
)


itos = SPECIAL_TOKENS.copy()

for token, freq in tokens:
    if token not in itos:
        itos.append(token)

stoi = {
    token: idx
    for idx, token in enumerate(itos)
}

PAD_IDX = stoi[PAD_TOKEN]
UNK_IDX = stoi[UNK_TOKEN]
BOS_IDX = stoi[BOS_TOKEN]
EOS_IDX = stoi[EOS_TOKEN]

VOCAB_SIZE = len(itos)

print("Vocabulary size:", VOCAB_SIZE)


# ------------------------------------------------------------
# 10. Numericalization
# ------------------------------------------------------------

def encode(text):
    tokens = tokenize(text)

    ids = [BOS_IDX]

    for token in tokens[:MAX_LEN - 2]:
        ids.append(stoi.get(token, UNK_IDX))

    ids.append(EOS_IDX)

    return ids


# ------------------------------------------------------------
# 11. Dataset
# ------------------------------------------------------------

class ChatbotDataset(Dataset):

    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        question = self.data.iloc[idx][question_col]
        answer = self.data.iloc[idx][answer_col]

        src = encode(question)
        tgt = encode(answer)

        return torch.tensor(src), torch.tensor(tgt)


# ------------------------------------------------------------
# 12. Padding Collate
# ------------------------------------------------------------

def collate_fn(batch):

    src_batch = []
    tgt_batch = []

    for src, tgt in batch:
        src_batch.append(src)
        tgt_batch.append(tgt)

    src_batch = nn.utils.rnn.pad_sequence(
        src_batch,
        batch_first=True,
        padding_value=PAD_IDX
    )

    tgt_batch = nn.utils.rnn.pad_sequence(
        tgt_batch,
        batch_first=True,
        padding_value=PAD_IDX
    )

    return src_batch, tgt_batch


train_dataset = ChatbotDataset(train_df)
valid_dataset = ChatbotDataset(valid_df)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=collate_fn
)

valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    collate_fn=collate_fn
)


# ------------------------------------------------------------
# 13. Positional Encoding
# ------------------------------------------------------------

class PositionalEncoding(nn.Module):

    def __init__(
        self,
        d_model,
        dropout=0.1,
        max_len=5000
    ):
        super().__init__()

        self.dropout = nn.Dropout(dropout)

        position = torch.arange(
            max_len
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                d_model,
                2
            ) * (-math.log(10000.0) / d_model)
        )

        pe = torch.zeros(
            max_len,
            d_model
        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        pe = pe.unsqueeze(0)

        self.register_buffer(
            "pe",
            pe
        )

    def forward(self, x):

        x = x + self.pe[:, :x.size(1)]

        return self.dropout(x)


# ------------------------------------------------------------
# 14. Transformer Seq2Seq Model
# ------------------------------------------------------------

class TransformerChatbot(nn.Module):

    def __init__(
        self,
        vocab_size,
        d_model=368,
        n_heads=8,
        n_layers=1,
        d_ff=1024,
        dropout=0.2
    ):
        super().__init__()

        self.d_model = d_model

        self.embedding = nn.Embedding(
            vocab_size,
            d_model,
            padding_idx=PAD_IDX
        )

        self.positional_encoding = PositionalEncoding(
            d_model,
            dropout
        )

        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=n_heads,
            num_encoder_layers=n_layers,
            num_decoder_layers=n_layers,
            dim_feedforward=d_ff,
            dropout=dropout,
            batch_first=True
        )

        self.output_layer = nn.Linear(
            d_model,
            vocab_size
        )

    def forward(
        self,
        src,
        tgt,
        src_key_padding_mask=None,
        tgt_key_padding_mask=None,
        tgt_mask=None
    ):

        src_emb = self.embedding(src) * math.sqrt(self.d_model)
        tgt_emb = self.embedding(tgt) * math.sqrt(self.d_model)

        src_emb = self.positional_encoding(src_emb)
        tgt_emb = self.positional_encoding(tgt_emb)

        output = self.transformer(
            src_emb,
            tgt_emb,
            tgt_mask=tgt_mask,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            memory_key_padding_mask=src_key_padding_mask
        )

        return self.output_layer(output)


model = TransformerChatbot(
    vocab_size=VOCAB_SIZE,
    d_model=D_MODEL,
    n_heads=N_HEADS,
    n_layers=N_LAYERS,
    d_ff=D_FF,
    dropout=DROPOUT
).to(device)

print(model)


# ------------------------------------------------------------
# 15. Causal Mask
# ------------------------------------------------------------

def generate_square_subsequent_mask(size):

    mask = torch.triu(
        torch.ones(
            size,
            size,
            device=device
        ),
        diagonal=1
    )

    mask = mask.masked_fill(
        mask == 1,
        float("-inf")
    )

    return mask


# ------------------------------------------------------------
# 16. Optimizer
# ------------------------------------------------------------

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1.0,
    betas=(0.9, 0.98),
    eps=1e-9
)


# ------------------------------------------------------------
# 17. Noam / Transformer Warmup Schedule
# ------------------------------------------------------------

def transformer_lr(step):

    step = max(step, 1)

    return (
        D_MODEL ** -0.5
        * min(
            step ** -0.5,
            step * WARMUP_STEPS ** -1.5
        )
    )


def update_learning_rate(step):

    lr = transformer_lr(step)

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr

    return lr


# ------------------------------------------------------------
# 18. Loss
# ------------------------------------------------------------

criterion = nn.CrossEntropyLoss(
    ignore_index=PAD_IDX
)


# ------------------------------------------------------------
# 19. Training
# ------------------------------------------------------------

def train_one_epoch():

    model.train()

    total_loss = 0

    for src, tgt in train_loader:

        src = src.to(device)
        tgt = tgt.to(device)

        tgt_input = tgt[:, :-1]
        tgt_output = tgt[:, 1:]

        tgt_mask = generate_square_subsequent_mask(
            tgt_input.size(1)
        )

        src_padding_mask = (
            src == PAD_IDX
        )

        tgt_padding_mask = (
            tgt_input == PAD_IDX
        )

        optimizer.zero_grad()

        logits = model(
            src,
            tgt_input,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=tgt_padding_mask,
            tgt_mask=tgt_mask
        )

        loss = criterion(
            logits.reshape(-1, VOCAB_SIZE),
            tgt_output.reshape(-1)
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            1.0
        )

        global global_step

        global_step += 1

        update_learning_rate(global_step)

        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


# ------------------------------------------------------------
# 20. Validation
# ------------------------------------------------------------

@torch.no_grad()
def evaluate():

    model.eval()

    total_loss = 0

    for src, tgt in valid_loader:

        src = src.to(device)
        tgt = tgt.to(device)

        tgt_input = tgt[:, :-1]
        tgt_output = tgt[:, 1:]

        tgt_mask = generate_square_subsequent_mask(
            tgt_input.size(1)
        )

        src_padding_mask = (
            src == PAD_IDX
        )

        tgt_padding_mask = (
            tgt_input == PAD_IDX
        )

        logits = model(
            src,
            tgt_input,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=tgt_padding_mask,
            tgt_mask=tgt_mask
        )

        loss = criterion(
            logits.reshape(-1, VOCAB_SIZE),
            tgt_output.reshape(-1)
        )

        total_loss += loss.item()

    return total_loss / len(valid_loader)


# ------------------------------------------------------------
# 21. Training Loop
# ------------------------------------------------------------

global_step = 0

best_valid_loss = float("inf")

for epoch in range(1, EPOCHS + 1):

    train_loss = train_one_epoch()
    valid_loss = evaluate()

    print(
        f"Epoch {epoch:02d}/{EPOCHS} | "
        f"Train Loss: {train_loss:.4f} | "
        f"Valid Loss: {valid_loss:.4f} | "
        f"LR: {optimizer.param_groups[0]['lr']:.8f}"
    )

    if valid_loss < best_valid_loss:

        best_valid_loss = valid_loss

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "stoi": stoi,
                "itos": itos,
                "vocab_size": VOCAB_SIZE,
                "hyperparameters": {
                    "n_layers": N_LAYERS,
                    "d_model": D_MODEL,
                    "n_heads": N_HEADS,
                    "d_ff": D_FF,
                    "dropout": DROPOUT,
                    "warmup_steps": WARMUP_STEPS,
                    "batch_size": BATCH_SIZE,
                    "epochs": EPOCHS
                }
            },
            "korean_chatbot_transformer.pt"
        )

        print("  -> Best model saved")


# ------------------------------------------------------------
# 22. Load Best Model
# ------------------------------------------------------------

checkpoint = torch.load(
    "korean_chatbot_transformer.pt",
    map_location=device
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

print("Best model loaded.")


# ------------------------------------------------------------
# 23. Greedy Decoding
# ------------------------------------------------------------

@torch.no_grad()
def generate_response(
    sentence,
    max_len=MAX_LEN
):

    model.eval()

    src = torch.tensor(
        [encode(sentence)],
        dtype=torch.long,
        device=device
    )

    src_padding_mask = (
        src == PAD_IDX
    )

    ys = torch.tensor(
        [[BOS_IDX]],
        dtype=torch.long,
        device=device
    )

    for _ in range(max_len):

        tgt_mask = generate_square_subsequent_mask(
            ys.size(1)
        )

        tgt_padding_mask = (
            ys == PAD_IDX
        )

        output = model(
            src,
            ys,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=tgt_padding_mask,
            tgt_mask=tgt_mask
        )

        next_token = output[:, -1, :].argmax(
            dim=-1
        ).item()

        ys = torch.cat(
            [
                ys,
                torch.tensor(
                    [[next_token]],
                    device=device
                )
            ],
            dim=1
        )

        if next_token == EOS_IDX:
            break

    result = []

    for idx in ys[0].tolist()[1:]:

        if idx in [
            EOS_IDX,
            PAD_IDX
        ]:
            break

        result.append(
            itos[idx]
        )

    return " ".join(result)


# ------------------------------------------------------------
# 24. Test
# ------------------------------------------------------------

test_sentences = [
    "지루하다, 놀러가고 싶어.",
    "오늘 일찍 일어났더니 피곤하다.",
    "간만에 여자친구랑 데이트 하기로 했어.",
    "집에 있는다는 소리야."
]

print("\n===== Chatbot Test =====")

for sentence in test_sentences:

    response = generate_response(sentence)

    print(f"\n입력 : {sentence}")
    print(f"응답 : {response}")