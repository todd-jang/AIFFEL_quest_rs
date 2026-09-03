# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 장기훈
- 리뷰어 : 조영근


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 노트북에는 KITTI semantic segmentation 데이터 다운로드 및 압축 해제, 이미지와 라벨의 매칭, 도로 클래스의 이진 마스크 변환, Albumentations 기반 전처리와 augmentation, PyTorch Dataset/DataLoader 구성, U-Net 학습, U-Net++ 학습, 모델 가중치 저장, 추론 결과 오버레이, IoU 계산, 두 모델의 평균 IoU 비교까지 포함되어 있습니다.
    - 특히 KittiDataset.__getitem__()에서 KITTI 라벨 값 7을 도로 영역으로 변환하고, 입력 텐서를 (H, W, C)에서 (C, H, W)로 변경하는 과정이 구현되어 있습니다. U-Net++에 대해서도 UNetPlusPlus 클래스를 직접 정의하고 model_path_unetpp에 가중치를 저장한 뒤 다시 불러와 평가하는 흐름이 연결되어 있습니다.
    - <img width="568" height="749" alt="image" src="https://github.com/user-attachments/assets/d33ba9ca-43d0-4ac9-908a-a8672d81c560" />

    
- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 가장 복잡한 부분은 U-Net++의 격자형 노드와 dense skip pathway를 구현한 UNetPlusPlus.forward()입니다. 해당 클래스의 docstring은 U-Net의 단순한 encoder-decoder skip connection과 달리, X_{i,j} 중간 노드를 두고 같은 depth의 이전 노드들과 하위 depth 노드의 upsampling 결과를 concat한다는 핵심 아이디어를 설명합니다. 또한 j=1, j=2, j=3, j=4 열별로 어떤 feature map을 결합하는지 주석이 있어 conv0_4까지 이어지는 구조를 추적하기 쉽습니다.
    - KittiDataset에도 클래스 설명과 생성자 인자 설명이 있고, 라벨의 이진화, 텐서 차원 변환, augmentation 적용 위치가 주석으로 구분되어 있습니다. 특히 추론 함수에서 라벨을 image가 아니라 mask로 전달해야 nearest interpolation이 적용된다는 수정 기록은 단순한 사용법을 넘어 라벨 오염을 방지하는 원인과 해결 방법을 설명하고 있어 좋은 부분입니다.
    - <img width="659" height="223" alt="image" src="https://github.com/user-attachments/assets/e3fd886a-84a0-472a-b3da-9e37afe1460f" />

        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - Albumentations 최신 버전에서 RandomSizedCrop의 인자 사용 방식이 달라질 수 있다는 점을 주석으로 기록했습니다.
    - segmentation mask에 일반 이미지와 같은 보간을 적용하면 클래스 라벨이 훼손될 수 있다는 문제를 발견하고, mask 인자로 전달하여 nearest interpolation을 사용하도록 수정했습니다.
    - get_output() 내부 입력 텐서는 CPU에 생성되는데 모델이 GPU에 있을 수 있다는 device mismatch 가능성을 인지하고, 비교 시점에 두 모델을 CPU로 이동하는 방어 코드를 추가했습니다.
    - <img width="731" height="517" alt="image" src="https://github.com/user-attachments/assets/32e0b742-9433-426b-b1f1-3b75d790d96a" />

        
- [x]  **4. 회고를 잘 작성했나요?**
    - 회고에서 U-Net은 구조가 단순하여 latency와 FPS 측면에서 유리하고, U-Net++는 더 복잡한 skip pathway 때문에 정밀한 segmentation에 적합하다는 trade-off를 자율주행 관점에서 설명했습니다.
    - 이는 모델 선택을 정확도만으로 판단하지 않고 실시간성 및 임베디드 환경까지 고려했다는 점에서 좋은 방향입니다.
    - <img width="747" height="316" alt="image" src="https://github.com/user-attachments/assets/0539b020-d58c-48e6-aa38-19eecdb9b694" />

        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - KittiDataset, UNet, UNetPlusPlus, calculate_iou_score, evaluate_mean_iou가 함수와 클래스로 분리되어 있어 핵심 기능의 재사용성은 좋습니다.
    - U-Net과 U-Net++에서 동일한 데이터셋과 optimizer 학습 패턴을 사용한 점도 비교 실험의 기준을 맞추려는 의도가 잘 드러납니다. U-Net++의 메모리 부담 때문에 batch size를 16에서 8로 줄인 판단도 현실적인 선택입니다.
    - <img width="557" height="455" alt="image" src="https://github.com/user-attachments/assets/77363e8e-13d7-49f7-baa8-acdc7490cfba" />


# 회고(참고 링크 및 코드 개선)
```
# 리뷰어의 회고를 작성합니다.
# 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
# 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.
```
