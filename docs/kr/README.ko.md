# AI 기반 이미지 초해상도 서비스 (Real-HAT-GAN)

## 🚀 프로젝트 개요

이 프로젝트는 웹 기반 AI 이미지 업스케일링 서비스를 제공합니다.  
최신 딥러닝 모델을 활용하여 이미지를 더욱 선명하고 정밀하게 향상시킵니다.  
백엔드는 FastAPI로 견고한 API를 제공하고, 프론트엔드는 누구나 사용하기 쉬운 웹 인터페이스로 구성되어 있습니다.

> 이 프로젝트는 개인 학습 목적을 위한 것이며, 상업적 용도로는 사용되지 않았습니다.

## ✨ 주요 기능

- **고화질 업스케일링**: Hybrid Attention Transformer (HAT) 모델을 사용하여 우수한 이미지 해상도 향상을 제공합니다.
- **모델 선택 기능**: 웹 인터페이스에서 다양한 HAT 모델(예: 범용형, 사실적 모델)을 선택하여 업스케일링할 수 있습니다.
- **웹 인터페이스 제공**: 이미지 업로드 및 업스케일링을 위한 직관적이고 간편한 웹 UI 제공.
- **RESTful API 제공**: FastAPI 기반의 깔끔하고 효율적인 API로 다른 애플리케이션과 쉽게 연동할 수 있습니다.
- **GPU 가속 지원**: NVIDIA GPU를 활용하여 빠른 이미지 처리 성능을 제공합니다.

## 🛠️ 사용 기술

- **백엔드**: Python, FastAPI, Uvicorn, PyTorch, BasicSR, GFPGAN, OpenCV, Pillow  
- **프론트엔드**: HTML, CSS, JavaScript  
- **AI 모델**: Hybrid Attention Transformer (HAT)

### Hybrid Attention Transformer (HAT) 모델

HAT 모델은 Transformer 아키텍처 기반의 최신 이미지 초해상도 모델입니다.  
이미지의 장기적인 의존 관계와 세밀한 디테일을 효과적으로 학습하여 매우 뛰어난 업스케일링 품질을 제공합니다.

이 프로젝트는 현재 여러 종류의 HAT 모델을 지원하며, 사용자가 원하는 업스케일링 스타일을 선택할 수 있습니다:

- **HAT_SRx4_ImageNet-pretrain.pth**: ImageNet 데이터셋으로 사전학습된 범용 HAT 모델로, 4배 업스케일링에 사용됩니다. 고정밀도이고 깔끔한 결과물을 생성하는 데 강점을 보입니다.
- **Real_HAT_GAN_SRx4.pth**: 보다 사실적이고 시각적으로 만족스러운 결과를 목표로 하는 GAN 기반 HAT 모델입니다. 역시 4배 업스케일링용이며, 질감과 디테일이 강조된 표현이 특징입니다. ImageNet 버전에 비해 예술적인 해석이 더해질 수 있습니다.

사용자는 웹 인터페이스에서 이 두 모델 중 원하는 것을 직접 선택할 수 있습니다.

## 📚 참고 자료

이 프로젝트는 아래의 오픈소스 프로젝트 및 연구 자료를 기반으로 통합 및 수정하여 개발되었습니다:

- **HAT (Hybrid Attention Transformer)**: HAT 모델의 공식 GitHub 저장소  
  (https://github.com/XPixelGroup/HAT)
- **BasicSR**: PyTorch 기반의 이미지 및 비디오 복원 툴킷. 많은 유틸리티 함수와 기본 클래스가 이 프로젝트에서 차용되었습니다.  
  (https://github.com/XPixelGroup/BasicSR)
- **Real-ESRGAN**: 실제 환경에 적합한 이미지 초해상도 알고리즘. RealESRGANer 유틸리티 클래스는 이 프로젝트에서 참고되었습니다.  
  (https://github.com/xinntao/Real-ESRGAN)

## 📂 프로젝트 구조

이 프로젝트는 프론트엔드와 백엔드를 명확히 분리하여 구성하였으며, 유지보수가 용이한 구조를 따르고 있습니다.

```
AI-Upscaling/
├── backend/ # AI 이미지 업스케일링을 위한 FastAPI 백엔드 애플리케이션
│ ├── init.py # 백엔드 Python 패키지 초기화 파일
│ ├── .env # 환경 변수 설정 파일 (예: 구성 관련)
│ ├── .gitignore # Git이 무시할 파일 목록 정의
│ ├── requirements.txt # 백엔드에서 필요한 Python 패키지 목록
│ ├── run.py # Uvicorn으로 FastAPI 앱을 실행하는 스크립트
│ ├── test_upscale.py # 업스케일링 기능에 대한 유닛 테스트 (구현된 경우)
│ ├── pycache/ # Python 바이트코드 캐시
│ ├── app/ # FastAPI 핵심 애플리케이션 로직
│ │ ├── init.py # 'app' 패키지 초기화 파일
│ │ ├── config.py # 모델 경로 및 설정을 포함한 전역 구성 파일
│ │ ├── main.py # FastAPI 앱의 진입점 및 CORS 설정
│ │ ├── pycache/ # 'app' 디렉토리의 바이트코드 캐시
│ │ ├── api/ # API 라우트 정의 디렉토리
│ │ │ ├── routes.py # 이미지 업스케일링 API 엔드포인트 정의
│ │ │ └── pycache/ # 'api' 디렉토리의 바이트코드 캐시
│ │ └── services/ # 비즈니스 로직 및 서비스 구현
│ │ ├── realesrgan_utils.py # Real-ESRGAN 관련 유틸리티 함수 및 모델 로딩
│ │ ├── upscale_service.py # 핵심 업스케일링 로직, AI 모델 로딩 및 관리
│ │ └── pycache/ # 'services' 디렉토리의 바이트코드 캐시
│ ├── model_weights/ # 사전학습된 AI 모델 가중치(.pth) 저장 디렉토리
│ └── models/ # 사용자 정의 AI 모델 구조 (예: HAT, SRVGG)
│ ├── init.py # 'models' 패키지 초기화 파일
│ ├── hat_arch.py # Hybrid Attention Transformer (HAT) 모델 구조 정의
│ ├── srvgg_arch.py # SRVGG 모델 구조 정의
│ └── pycache/ # 'models' 디렉토리의 바이트코드 캐시
├── frontend/ # 사용자 상호작용을 위한 웹 프론트엔드 파일
│ ├── index.html # 웹 인터페이스의 메인 HTML 페이지
│ ├── script.js # API 호출 및 동적 프론트엔드 동작을 위한 JavaScript
│ └── style.css # 웹 인터페이스 스타일을 위한 CSS
├── venv/ # Python 가상환경 디렉토리 (.gitignore로 제외됨)
│ ├── Include/... # 표준 가상환경 디렉토리 구조
│ ├── Lib/...
│ ├── Scripts/...
│ └── share/...
├── .gitignore # Git에서 제외할 파일 및 폴더 지정
├── README.md # 프로젝트 설명 파일 (현재 이 파일)
└── .git/ # Git 버전 관리 메타데이터
```


## ⚙️ 설치 및 실행 방법

이 프로젝트를 로컬에서 실행하기 위해 다음 단계를 따라주세요.

### 사전 준비 사항

-   Python 3.8 이상 (Python 3.10 이상 권장)
-   Git
-   **CUDA Toolkit 12.x가 설치된 NVIDIA GPU**  
    이 프로젝트는 GPU 가속을 전제로 구성되어 있으며, 호환 가능한 환경이 필요합니다.

### 실행 절차

1.  **레포지토리 클론:**
    ```bash
    git clone https://github.com/kosonkh7/AI-Upscaling.git
    cd AI-Upscaling
    ```

2.  **가상환경 생성 및 활성화:**
    ```bash
    # 가상환경 생성
    python -m venv venv

    # 가상환경 활성화
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **백엔드 의존성 설치:**
    `requirements.txt`는 CUDA 12.x 환경과의 호환을 고려하여 GitHub에서 직접 일부 라이브러리를 설치하도록 구성되어 있습니다.
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **GPU 사용 가능 여부 확인:**
    설치 후 아래 명령어를 실행하여 PyTorch가 GPU를 인식하는지 확인합니다.
    ```python
    python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
    ```
    출력 결과가 `GPU Available: True`여야 합니다.  
    `False`일 경우, NVIDIA 드라이버 및 CUDA Toolkit 설치를 다시 확인해 주세요.

5.  **모델 가중치 다운로드 및 배치:**
    프로젝트에서는 여러 HAT 모델을 사용합니다. 사전 학습된 모델 가중치를 다운로드한 후 `backend/model_weights/` 디렉토리에 저장하세요.
    -   **HAT_SRx4_ImageNet-pretrain.pth**: [다운로드 링크](https://www.kaggle.com/datasets/djokester/hat-pre-trained-weights?resource=download)
    -   **Real_HAT_GAN_SRx4.pth**: [다운로드 링크](https://www.kaggle.com/datasets/djokester/hat-pre-trained-weights?resource=download)
    -   **모델 위치**: 다운로드한 파일을 `backend/model_weights/` 경로에 저장하세요.

## 🚀 사용 방법

서비스를 실행하려면 백엔드 서버를 시작해야 합니다.  
또는 **Docker 이미지**를 사용하여 실행할 수도 있습니다.

### 백엔드 API 서버 실행

프로젝트 루트 디렉토리에서 FastAPI 애플리케이션을 실행하세요.

```bash
python backend/run.py

백엔드 API는 http://127.0.0.1:8000 에서 실행되며, 터미널에서 Uvicorn 로그를 확인할 수 있습니다.
```

### Docker 컨테이너로 실행

새 터미널에서 다음 명령어를 통해 Docker 컨테이너를 실행하세요.

```docker
docker pull kosonkh7/aisr-upscaler-gpu:v0.0.0
docker run --gpus all -d -p 8000:8000 kosonkh7/aisr-upscaler-gpu:v0.0.0
```

이 방식 역시 http://127.0.0.1:8000 주소에서 실행됩니다.

이제 웹 인터페이스를 통해 이미지를 업로드하고 업스케일링할 수 있습니다.

## 🔧 문제 해결

- **`ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor'`**
  - **원인**: PyPI에서 설치한 `basicsr` 또는 `gfpgan`의 표준 버전이 최신 `torchvision`과 호환되지 않아 발생하는 오류입니다.  
    `functional_tensor` 모듈은 최신 `torchvision` 버전에서 리팩터링되었습니다.
  - **해결 방법**: 이 프로젝트의 `requirements.txt` 파일은 해당 라이브러리들을 공식 GitHub 저장소에서 직접 설치하여, 최신 `torchvision`과의 호환 문제를 해결하도록 구성되어 있습니다.  
    이 오류가 발생했다면 아래 명령어를 사용하여 의존성을 정확히 설치했는지 확인해 주세요.

    ```bash
    pip install -r backend/requirements.txt
    ```

## 💡 향후 개선 사항

- **메모리 효율화**: GPU 메모리 사용을 최적화하고, 배치 및 이미지 크기 처리를 개선하여 CUDA 메모리 부족(OOM) 문제를 해결
- **모델 다양화**: 얼굴, 일러스트 등 다양한 이미지 유형에 특화된 모델을 통합하여 도메인별 품질 향상
- **성능 최적화**: ONNX 또는 TensorRT 변환을 통해 업스케일링 속도 향상
- **사용자 경험 개선**: 진행률 표시기, 전/후 비교 기능 등 프론트엔드의 편의성 향상

## 🤝 기여

이 프로젝트는 누구나 기여할 수 있습니다.  
이슈를 등록하거나 Pull Request를 자유롭게 제출해 주세요.
