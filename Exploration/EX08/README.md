# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 조영근


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 뉴스 기사 텍스트 요약을 위한 데이터 전처리, 모델 구축, 학습, 평가 및 비교 분석 과정이 빠짐없이 체계적으로 구현되었음
    - 학습 및 검증 손실(Loss) 감소 그래프를 통해 모델 학습이 성공적으로 진행되었음을 확인
    - <img width="2700" height="1500" alt="image" src="https://github.com/user-attachments/assets/a87861aa-9eaa-4821-bafe-24a982516083" />
    - 설명이나 이해가 필요한 부분에 적절히 주석이 사용
    - <img width="607" height="165" alt="image" src="https://github.com/user-attachments/assets/a2d5d31e-1ce5-408f-a82c-4c7132d81ffa" />

- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - Encoder-Decoder 구조에 Attention 메커니즘을 결합한 추상적 요약(Abstractive Summarization) 모델 구축 과정
    - TextRank 기반 추출적 요약(Extractive Summarization) 구현 부에 상세한 주석과 함수 설명이 작성
    - <img width="729" height="478" alt="image" src="https://github.com/user-attachments/assets/25d3e178-c308-4fcf-82bc-27f021759498" />
        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - LSTM 기반 Seq2Seq 모델의 한계점을 정확히 진단
    - 해결하기 위해 HuggingFace의 사전 학습된 Transformer 모델을 도입
    - 추가 실험 및 비교를 수행한 점
    - <img width="752" height="607" alt="image" src="https://github.com/user-attachments/assets/639a9f02-3f60-43ee-9474-bac9931e6e3e" />

- [x]  **4. 회고를 잘 작성했나요?**
    - Abstractive 요약과 Extractive 요약의 결과를 문법 완성도와 핵심 단어 포함 측면에서 정량적으로 비교하고, 표를 통해 체계적으로 정리
    - <img width="2700" height="1050" alt="image" src="https://github.com/user-attachments/assets/e0edf45d-af57-4738-ad5e-9d9e6bb477ed" />
    - 모델의 한계점 분석과 향후 개선 방향을 정리
    - <img width="764" height="436" alt="image" src="https://github.com/user-attachments/assets/e79b8c05-5d0e-4746-aa19-e6c2824daf4d" />

        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - 데이터 전처리, 정제, 정규화, 불용어 제거 및 인코딩 과정이 함수화 및 파이프라인 형태로 구조화되어 있어 코드의 가독성과 재사용성이 높음
    - <img width="775" height="700" alt="image" src="https://github.com/user-attachments/assets/8bde11d7-d257-42ae-afd0-305d772d492b" />

# 회고(참고 링크 및 코드 개선)
```
# 리뷰어의 회고를 작성합니다.
# 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
# 코드 리뷰
