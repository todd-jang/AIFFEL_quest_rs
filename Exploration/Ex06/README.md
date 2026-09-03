# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 조영근


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - NSMC(Naver Sentiment Movie Corpus) 한국어 감성분석 데이터를 활용하여 총 4가지 모델(TF-IDF + Logistic Regression, TF-IDF + LinearSVC, CNN + Word2Vec, BiLSTM + Word2Vec)을 구현하고 평가를 완료했습니다.
    - 모델별 Accuracy, Precision, Recall, F1-score를 계산하고 최종 성능 비교표 및 시각화를 충실히 수행하였습니다.
    - <img width="527" height="667" alt="image" src="https://github.com/user-attachments/assets/f79005b8-a36f-4bc0-a859-42ab0228eba1" />

    
- [ ]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 각 Cell을 시작할 때 역할만 주석으로 처리하였습니다.
    - <img width="462" height="58" alt="image" src="https://github.com/user-attachments/assets/7bf94fdb-80ac-4417-b318-c0ba59797e5b" />

        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 4개 모델의 성능을 비교하기 위해 Accuracy와 F1-score를 85%, 90% 기준선이 포함된 바 차트로 시각화하였습니다.
    - 각 모델별 Confusion Matrix를 도출하여 오분류 경향을 심층 분석했습니다.
    - 자체학습 Word2Vec 임베딩 외에도 사전학습 Word2Vec(pre-trained .bin) 파일과의 비교를 수행할 수 있는 확장 코드를 포함하여 의미공간의 차이를 비교할 수 있도록 시도하였습니다.
    - 자동 체크리스트 검증 로직을 통해 목표 정확도(85% 이상) 달성 여부를 프로그래밍 방식으로 확인했습니다.
    - <img width="596" height="549" alt="image" src="https://github.com/user-attachments/assets/f419619b-0698-426f-a2b5-0e52a77771d5" />
    - 프로젝트의 조건에 주어진 형태소 분석기는 Mecab으로 작성되었으면 더 성능이 좋은 모델이 나왔을 것 같습니다.
    - 데이터 전처리부터 형태소 분석기(Okt) 적용한 부분이 아쉽습니다.
    - <img width="473" height="237" alt="image" src="https://github.com/user-attachments/assets/73e23b63-0359-4150-af37-a8418fa220e0" />

        
- [x]  **4. 회고를 잘 작성했나요?**
    - 전통적인 머신러닝 모델(TF-IDF + Linear 모델)과 딥러닝 모델(Word2Vec 기반 CNN, BiLSTM)의 장단점 및 성능 차이에 대한 고찰이 잘 드러나 있습니다.
    - 데이터 전처리(형태소 분석기 Okt 활용, 불용어 제거, 시퀀스 패딩)부터 모델 학습, 평가 및 시각화까지의 전체 파이프라인이 논리적으로 구성되어 있습니다.
    - <img width="769" height="546" alt="image" src="https://github.com/user-attachments/assets/348dcfc1-3dba-47bd-99b3-87e309871e1b" />

        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - PyTorch 모델의 학습 및 평가를 위한 공통 함수(train_torch_model, predict_torch, plot_training)를 구현하여 코드 중복을 최소화하고 가독성을 높였습니다.
    - Pandas DataFrame을 활용한 결과 정렬 및 스타일링(display(results.style.format(...)))을 통해 분석 결과를 깔끔하게 확인하도록 작성되었습니다.
    - <img width="462" height="270" alt="image" src="https://github.com/user-attachments/assets/b1ea8cc8-e1f4-4e89-a314-c2b717912856" />


# 회고(참고 링크 및 코드 개선)
```
# NSMC 데이터셋을 대상으로 전통적 기법(TF-IDF + 머신러닝)부터 최신 임베딩 기반 딥러닝 기법(Word2Vec + CNN/BiLSTM)까지 종합적으로 비교·분석하였습니다.
```
