# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 김나연


# PRT(Peer Review Template)
- [X]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 구두점, 대소문자, 띄어쓰기, 한글 형태소분석 등 번역기 모델에 요구되는 전처리가 정상적으로 진행되었다.
        - <img width="1446" height="737" alt="image" src="https://github.com/user-attachments/assets/d2810785-458b-4af0-9480-f75c5653077f" />
    - seq2seq 모델 훈련 과정에서 training loss가 안정적으로 떨어지면서 학습이 진행됨이 확인되었다.
        - <img width="861" height="568" alt="image" src="https://github.com/user-attachments/assets/b152e09d-29e6-4ac9-82ce-6bbdf6da87fd" />
    - 테스트용 디코더 모델이 정상적으로 만들어져서, 정답과 어느 정도 유사한 영어 번역이 진행됨을 확인하였다.
        - <img width="641" height="307" alt="image" src="https://github.com/user-attachments/assets/4f7f1cf1-cb8c-49c4-98c5-81414dc6f415" />
    
- [X]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 실행 과정에 대해 텍스트로 설명하고 있다.
        - <img width="898" height="263" alt="image" src="https://github.com/user-attachments/assets/919c6091-d393-4477-863a-acc441870eff" />
        - <img width="1045" height="256" alt="image" src="https://github.com/user-attachments/assets/4480b99b-8c62-4284-83a6-aad25d67ddb4" />
        
- [ ]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 
        
- [ ]  **4. 회고를 잘 작성했나요?**
    - 
        
- [X]  **5. 코드가 간결하고 효율적인가요?**
    - 전처리, 토큰화, 데이터셋, Attention, Encoder, Decoder, 학습, 평가, 번역 기능이 함수와 클래스로 분리되어 있다.
        - <img width="1791" height="717" alt="image" src="https://github.com/user-attachments/assets/491cc867-eb2a-4a60-8f02-24cfdbe5b6c4" />

# 회고(참고 링크 및 코드 개선)
```
Greedy Search와 Beam Search의 차이인건지 저보다 예문을 번역한 결과가 더 좋아서 신기합니다!
```
