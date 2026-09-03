# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈   
- 리뷰어 : 이민서


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**

    5 epoch 동안 loss가 단조 감소하고 accuracy가 0.09 → 0.91로 올라가 안정적으로 수렴하는 과정을 보여주었습니다.
   <img width="733" height="222" alt="image" src="https://github.com/user-attachments/assets/36d671df-9c02-4864-b7d3-566e90652d59" />

   테스트셋 960장 전체에 대해 accuracy / mean IoU / IoU≥0.5 비율을 두 방법 각각 계산했습니다.
    <img width="905" height="108" alt="image" src="https://github.com/user-attachments/assets/6fa7ae2f-624f-477f-9df4-af75bf057537" />

    다만 학습 루프에 validation loop가 없어 epoch별 일반화 추이는 확인이 어려웠습니다.

    
- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
  
    코드보다 먼저 CAM의 수식과 구조적 제약을 명시해 두어서, 아래 코드의 weight[:, :, None, None] * self.activation 한 줄이 왜 그렇게 생겼는지 바로 이해할 수 있었습니다.
    <img width="1885" height="388" alt="image" src="https://github.com/user-attachments/assets/43a9e04b-db78-4cc9-be2d-5449c2d284fa" />

    주석이 왜 필요한지를 적고 있어서 이해하기가 편했습니다.
    <img width="1429" height="888" alt="image" src="https://github.com/user-attachments/assets/314182e8-1bb8-443a-9d2c-bb280be54dc1" />

        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**

     디버깅 기록은 인라인 주석 형태로 남아 있습니다.
    <img width="1242" height="466" alt="image" src="https://github.com/user-attachments/assets/8a6e9f96-507d-44fd-a32e-585cb66a2412" />
    <img width="1428" height="880" alt="image" src="https://github.com/user-attachments/assets/9bde986b-8729-466e-992c-90a7f9589211" />

    아쉬운 점: 셀 22 출력에 Heatmap Min/Max: 0.0 0.0 이 남아 있고 주석에도 "Max가 1.0 부근이어야 정상"이라고 적어 두셨는데, 비정상이라는 걸 인지한 상태에서 원인 추적이 멈춰 있습니다.
    <img width="1261" height="746" alt="image" src="https://github.com/user-attachments/assets/0446fb0f-f71b-494b-b404-288e553469f0" />

        
- [x]  **4. 회고를 잘 작성했나요?**

    셀 33에서 두 방법의 accuracy가 동일하게 나온 이유를 "수학적 일치"로 설명한 부분은 정확합니다. 배운 점 / 느낀 점이 빠져 있는 점은 아쉽습니다.  
    <img width="1854" height="650" alt="image" src="https://github.com/user-attachments/assets/f79fcd01-4014-4c28-8ebb-7b24c56ada6a" />

        
- [x]  **5. 코드가 간결하고 효율적인가요?**

    시각화/평가 로직이 전부 함수와 클래스로 분리되어 재사용됩니다. 특히 evaluate가 엔진 클래스를 인자로 받아 CAM/Grad-CAM에 동일하게 적용되는 구조가 깔끔했습니다.
    <img width="811" height="1125" alt="image" src="https://github.com/user-attachments/assets/273e1b4e-5eaf-49c6-9daf-77a04a24c771" />



# 회고(참고 링크 및 코드 개선)

* Heatmap Min/Max: 0.0 0.0 의 원인 — ReLU 이후에 정규화하기 때문입니다

현재 코드는 ReLU → max로 나누기 순서입니다. 예측 클래스의 가중합이 모든 위치에서 음수인 샘플(학습이 짧은 linear probe에서 종종 발생)은 ReLU에서 전부 0이 되고, heat / (0 + 1e-8) 이 그대로 0 맵이 됩니다. 그 결과 mask_to_box가 None을 반환하고 IoU가 0으로 집계되어 mean_iou 0.1805를 실제보다 낮게 만듭니다.

정규화를 ReLU 앞으로 옮기고 min-max로 바꾸면 전멸 맵이 사라집니다.
