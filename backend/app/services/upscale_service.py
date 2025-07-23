import torch
import cv2
import numpy as np
from models.hat_arch import HAT
from .realesrgan_utils import RealESRGANer
from PIL import Image
import io

# config.py에서 모델 설정 가져오기
from ..config import AVAILABLE_MODELS, UPSCALE_SCALE

class UpscaleService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UpscaleService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print("Initializing UpscaleService and loading models...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.upsamplers = {}

        # AVAILABLE_MODELS에 정의된 모든 모델을 로드
        for model_key, config in AVAILABLE_MODELS.items():
            print(f"Loading model: {config['name']} ({model_key})...")
            try:
                # HAT 모델 아키텍처는 동일하다고 가정하고 인스턴스화
                # 참고: 만약 모델별로 아키텍처 파라미터가 다르다면, 이 부분을 수정해야 함
                model = HAT(
                    upscale=UPSCALE_SCALE,
                    in_chans=3,
                    img_size=64,
                    window_size=16,
                    embed_dim=180,
                    depths=[6, 6, 6, 6, 6, 6],
                    num_heads=[6, 6, 6, 6, 6, 6],
                    compress_ratio=3,
                    squeeze_factor=30,
                    conv_scale=0.01,
                    overlap_ratio=0.5,
                    mlp_ratio=2.0,
                    qkv_bias=True,
                    qk_scale=None,
                    drop_rate=0.0,
                    attn_drop_rate=0.0,
                    drop_path_rate=0.1,
                    norm_layer=torch.nn.LayerNorm,
                    ape=False,
                    patch_norm=True,
                    use_checkpoint=False,
                    img_range=1.0,
                    upsampler='pixelshuffle',
                    resi_connection='1conv'
                )

                upsampler = RealESRGANer(
                    scale=UPSCALE_SCALE,
                    model_path=config['path'],
                    model=model,
                    model_type=config['type'],  # 모델 타입 전달
                    tile=0,
                    tile_pad=10,
                    pre_pad=0,
                    half=False,  # 데이터 타입 충돌을 피하기 위해 half-precision 비활성화
                    model_input_divisible_by=16
                )
                self.upsamplers[model_key] = upsampler
                print(f"Model '{config['name']}' loaded successfully on {self.device}.")
            except Exception as e:
                print(f"Error loading model {config['name']}: {e}")

    async def upscale_image(self, image_bytes: bytes, model_name: str) -> bytes:
        """
        주어진 모델 이름에 따라 적절한 업스케일러를 사용하여 이미지를 업스케일링합니다.
        """
        if model_name not in self.upsamplers:
            raise ValueError(f"Model '{model_name}' is not available.")

        upsampler = self.upsamplers[model_name]

        try:
            img_pil = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            img_np = np.array(img_pil)
            img_np_bgr = img_np[:, :, [2, 1, 0]]

            output_img, _ = upsampler.enhance(img_np_bgr, outscale=UPSCALE_SCALE)

            output_img_rgb = output_img[:, :, [2, 1, 0]]
            upscaled_pil = Image.fromarray(output_img_rgb)

            img_byte_arr = io.BytesIO()
            upscaled_pil.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()

        except Exception as e:
            print(f"Error during image upscaling with model {model_name}: {e}")
            raise

# 서비스 인스턴스 생성 (싱글톤)
upscale_service = UpscaleService()
