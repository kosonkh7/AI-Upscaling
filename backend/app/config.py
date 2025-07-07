import os

# 프로젝트 루트 디렉토리 (AI-Upscaling)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 업스케일링 스케일
UPSCALE_SCALE = 4

# 사용 가능한 업스케일링 모델 정의
AVAILABLE_MODELS = {
    "HAT_SRx4_ImageNet-pretrain": {
        "name": "HAT (ImageNet-pretrain)",
        "path": os.path.join(BASE_DIR, "backend", "model_weights", "HAT_SRx4_ImageNet-pretrain.pth"),
        "type": "standard",  # 일반 체크포인트
    },
    "Real_HAT_GAN_SRx4": {
        "name": "Real-HAT (GAN)",
        "path": os.path.join(BASE_DIR, "backend", "model_weights", "Real_HAT_GAN_SRx4.pth"),
        "type": "gan",  # GAN 모델 (generator 가중치 필요)
    }
}
