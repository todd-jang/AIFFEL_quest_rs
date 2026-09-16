# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 조영근


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 최종 프로젝트 구간에서 데이터부터 모델 학습과 결과 시각화까지의 전체 흐름이 연결되어 있습니다.
        - **데이터 확보 및 전처리**: `wikimedia/wikipedia`의 한국어 코퍼스를 내려받고 `kowiki.txt`로 저장합니다. 이미 파일이 있으면 재사용하도록 조건문도 작성되어 있습니다.
        - **Tokenizer 구성**: `vocab_size=8000`, `model_type="bpe"`로 SentencePiece를 학습합니다. `[PAD]`, `[UNK]`, `[CLS]`, `[SEP]`, `[MASK]` 특수 토큰도 지정되어 있습니다.
        - **MLM/NSP 데이터셋 생성**: `create_and_save_memmap()` 함수에서 입력 토큰, segment, attention mask, MLM label, NSP label을 각각 memmap 파일에 기록합니다. 실행 결과로 `총 생성된 샘플 수: 20000`이 출력됩니다.
        - **모델 구현**: embedding, Transformer encoder, NSP head, MLM head를 구성합니다.
        - **학습 및 결과 확인**: 50 epoch 동안 학습하고 total loss, MLM loss, NSP loss, MLM accuracy, NSP accuracy를 기록합니다. loss/accuracy 그래프를 `kowiki_bert_pretraining_metrics.png`로 저장하고 화면에도 출력합니다.
        - **학습 산출물**: 마지막 출력에서 50 epoch 결과가 확인됩니다.
        - <img width="770" height="98" alt="image" src="https://github.com/user-attachments/assets/cd4c465f-e1cb-4719-bf2f-9f826e033c37" />
        - <img width="1489" height="490" alt="image" src="https://github.com/user-attachments/assets/e3137b51-fba2-4a35-bcf6-15fb49b91eed" />
        - <img width="977" height="56" alt="image" src="https://github.com/user-attachments/assets/d50ab1b1-a30e-4a86-a3bc-83e1460fdae0" />
    
- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 가장 핵심적인 부분은 **MLM/NSP 학습 샘플을 만들고 대용량 파일을 memmap으로 저장하는 전처리 과정**과 **두 개의 pretraining head를 동시에 학습하는 모델·학습 루프**입니다. 이 부분은 데이터 구조와 학습 목적을 함께 이해해야 하므로 전체 코드에서 가장 복잡한 구간으로 판단했습니다.
    - <img width="811" height="336" alt="image" src="https://github.com/user-attachments/assets/d25f8272-8a5c-4a04-a351-cce8ff79bb54" />
        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나 새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 코드 자체에서 수정과 추가 시도의 흔적은 확인됩니다.
    - <img width="713" height="296" alt="image" src="https://github.com/user-attachments/assets/4c634c57-b0bf-437e-8870-6a417f15880c" />

- []  **4. 회고를 잘 작성했나요?**
    - loss 및 accuracy 그래프가 생성되고, 학습 로그가 충분히 남아 있습니다. 하지만 회고 내용을 작성하지 않았습니다.
        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - 효율성을 고려한 설계는 분명히 확인됩니다.
        - 대용량 전처리를 파일 스트리밍 방식으로 처리합니다.
        - `np.memmap`을 이용해 입력, segment, attention mask, label을 RAM에 전부 적재하지 않습니다.
        - `MemmapBERTDataset`은 PyTorch `Dataset` 인터페이스를 구현하고, `DataLoader(batch_size=32, shuffle=True)`로 배치 학습을 수행합니다.
        - `BERTConfig`를 사용해 vocabulary 크기, hidden dimension, layer 수, head 수, sequence 길이를 한 곳에서 관리합니다.
        - `MiniBERTForPreTraining`을 클래스화해 모델 구성과 forward 연산을 분리했습니다.
        - MLM decoder와 token embedding의 weight tying을 사용합니다.했는지 확인
        - <img width="784" height="554" alt="image" src="https://github.com/user-attachments/assets/717bb9db-db19-4e33-a7ff-21fad2713818" />

# 회고(참고 링크 및 코드 개선)
```
# BERT의 pretraining 과정을 데이터 생성부터 모델 학습까지 직접 구현했다는 점이 강점이다.
# 특히 8,000 vocabulary와 941,794개 파라미터의 mini-BERT를 구성하고, 20,000개 샘플을 memmap으로 처리한 결과는 프로젝트 목표에 직접 대응한다.
