# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 김나연


# PRT(Peer Review Template)
- [X]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 코퍼스 분석, 전처리, SentencePiece 적용, 토크나이저 구현 및 동작이 빠짐없이 진행되었습니다.
        - <img width="1168" height="346" alt="image" src="https://github.com/user-attachments/assets/7faf07fc-5b56-4746-8108-70b76cd95028" />
        - <img width="902" height="440" alt="image" src="https://github.com/user-attachments/assets/09504c4e-a0fe-4a3b-93c2-d599ea967284" />
    - SentencePiece 토크나이저가 적용된 Text Classifier 모델이 정상적으로 수렴하여 80% 이상의 test accuracy가 확인되었습니다.
        - <img width="603" height="536" alt="image" src="https://github.com/user-attachments/assets/0cf2b714-c043-459f-9b85-831a7bd940ec" />
    - SentencePiece 토크나이저를 활용했을 때의 성능을 다른 토크나이저 혹은 SentencePiece의 다른 옵션의 경우와 비교하여 분석을 체계적으로 진행하였습니다.
        - <img width="891" height="500" alt="image" src="https://github.com/user-attachments/assets/fbb7c7f4-9387-48b1-a4f0-25e019612f2c" />
        - <img width="1125" height="506" alt="image" src="https://github.com/user-attachments/assets/743a3f9e-e33a-4513-967d-9374c4e4e7b7" />
    
- [X]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 코드 작성 중간 중간에 주석을 첨부해 이해를 돕고 있다.
        - <img width="1166" height="753" alt="image" src="https://github.com/user-attachments/assets/543023be-62dd-4f3a-bc00-6a103615a739" />

        
- [ ]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 문제 원인 및 해결 과정을 잘 기록하였는지 확인
    - 프로젝트 평가 기준에 더해 추가적으로 수행한 나만의 시도, 
    실험이 기록되어 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [X]  **4. 회고를 잘 작성했나요?**
    - 감성 분석 테스트 결과와 실험 결과를 표와 그래프를 이용해 적절히 표현하였다.
        - <img width="757" height="718" alt="image" src="https://github.com/user-attachments/assets/2baa022c-4ae7-4d28-9276-88987a716215" />
        - <img width="859" height="682" alt="image" src="https://github.com/user-attachments/assets/19914f61-cf38-46c1-b705-683adad750b9" />
        
- [X]  **5. 코드가 간결하고 효율적인가요?**
    - 코드 중복을 최소화하고 범용적으로 사용할 수 있도록 함수화 하였다.
        - <img width="739" height="585" alt="image" src="https://github.com/user-attachments/assets/9f8d2a83-ce21-4fa1-a1e2-f552b9bb7359" />
        - <img width="754" height="338" alt="image" src="https://github.com/user-attachments/assets/1e518197-9df9-46c8-bc5d-143d77c0910c" />




# 회고(참고 링크 및 코드 개선)
```
전처리 과정 수행 전에 EDA 과정이 추가로 있었으면 더 좋았겠다라는 생각이 듭니다.
```
