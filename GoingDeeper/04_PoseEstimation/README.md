# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 조영근


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 노트북에는 MPII 데이터셋 다운로드 및 파싱, 데이터 전처리, TFRecord/PT record 생성, DataLoader 구성, heatmap 생성, Stacked Hourglass 모델 구현, SimpleBaseline 모델 구현, 학습 엔진, 체크포인트 저장 및 로드, 테스트 이미지에 대한 pose estimation, 두 모델의 정량적·정성적 비교까지 전체 실행 흐름이 포함되어 있습니다.
    - 모든 코드 셀에 실행 결과가 저장되어 있고 오류 출력도 확인되지 않았습니다.
    - 특히 프로젝트 단계에서 두 모델을 동일하게 5 epoch씩 학습했으며, epoch당 학습 시간도 비교했습니다.
    - 실행 결과상 Hourglass는 epoch당 약 8.3분, SimpleBaseline은 약 3.5분으로 모두 30분 이내에 학습되었습니다.
    - 또한 최종 비교표에서 Hourglass의 최저 validation loss는 1.1523, SimpleBaseline은 0.2719로 기록되어 있습니다.
    - 테스트 이미지에 대해 두 모델의 skeleton/keypoint 결과와 관절별 heatmap 이미지도 출력되어 있어, 단순히 모델을 정의하는 수준을 넘어 문제 해결에 필요한 결과물까지 제출된 것으로 판단됩니다.
    - <img width="714" height="278" alt="image" src="https://github.com/user-attachments/assets/fc8c9e07-95f9-417b-adb1-07d6034ce8d8" />

    
- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 가장 복잡한 부분인 Stacked Hourglass 네트워크, 중간 loss를 포함한 학습 엔진, 데이터 전처리 및 체크포인트 로딩 함수에 주석과 docstring이 비교적 잘 작성되어 있습니다.
    - <img width="767" height="590" alt="image" src="https://github.com/user-attachments/assets/a192252a-58d5-4623-8db8-35db878de829" />
        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 명시적인 오류 로그와 상세한 디버깅 일지가 길게 기록된 형태는 아니지만, 새로운 시도와 추가 실험은 충분히 확인됩니다.
    - 기본 Stacked Hourglass 모델만 실행한 것이 아니라 SimpleBaseline 모델을 별도로 구현하고, 두 모델을 동일한 epoch 수와 비교 조건으로 학습하여 성능과 속도를 비교했습니다.
    - 비교 과정에서 loss curve, epoch당 소요 시간, skeleton/keypoint 시각화, 선택 관절의 heatmap, 최종 loss 요약표를 모두 추가하여 정량적·정성적 분석을 수행했습니다.
    - <img width="728" height="137" alt="image" src="https://github.com/user-attachments/assets/89b12230-45df-4a55-8eea-37f0f69a5c5b" />


        
- [x]  **4. 회고를 잘 작성했나요?**
    - 회고 내용은 작성되어 있으며, SimpleBaseline이 ImageNet 사전학습 ResNet-50 backbone을 활용하고 Stacked Hourglass는 주요 모듈을 직접 학습한다는 차이를 바탕으로 두 모델의 수렴 속도와 성능 차이를 해석하고 있습니다.
    - 또한 몸통에서 먼 관절의 heatmap이 상대적으로 불확실하게 나타나는 현상과 SimpleBaseline의 관절 표현 차이에 대해서도 관찰을 남겼습니다.
    - 따라서 배운 점과 실험 결과에 대한 해석은 포함되어 있습니다.
    - <img width="1326" height="248" alt="image" src="https://github.com/user-attachments/assets/7873765e-f32f-4a0b-8b62-41a642fed777" />

        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - 코드는 데이터 처리, 모델 구성, 학습, 예측, 시각화 기능을 함수와 클래스로 나누어 작성되어 있으며, DataLoader, sharding/PT record, Ray 기반 병렬 처리 등을 활용해 대규모 MPII 데이터를 효율적으로 다루려는 시도가 보입니다.
    - 특히 BottleneckBlock, HourglassModule, Preprocessor, Trainer, MPIIDataset처럼 역할별 추상화가 이루어져 있어 코드 재사용성과 유지보수성이 좋습니다.
    - 두 모델의 비교도 동일한 학습 함수와 공통 평가 흐름을 사용해 중복을 줄였습니다.
    - <img width="841" height="507" alt="image" src="https://github.com/user-attachments/assets/921a2783-354a-4685-bca2-b3f719f66cee" />



# 회고(참고 링크 및 코드 개선)
```
# 리뷰어의 회고를 작성합니다.
# 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
# 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.
```
