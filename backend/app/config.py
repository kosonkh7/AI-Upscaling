import os

# 프로젝트 루트 디렉토리 (AI-Upscaling)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 모델 파일 경로
HAT_MODEL_PATH = os.path.join(BASE_DIR, "backend", "model_weights", "HAT_SRx4_ImageNet-pretrain.pth")

# 업스케일링 스케일 (HAT_SRx4_ImageNet-pretrain.pth는 4배 업스케일링 모델)
UPSCALE_SCALE = 4
