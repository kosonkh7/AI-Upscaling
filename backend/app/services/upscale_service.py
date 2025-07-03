import torch
import cv2
import numpy as np
from backend.models.hat_arch import HAT as HAT
from basicsr.utils.img_util import img2tensor, tensor2img
from backend.app.services.realesrgan_utils import RealESRGANer
from basicsr.data.transforms import mod_crop
from PIL import Image
import io

from ..config import HAT_MODEL_PATH, UPSCALE_SCALE

class UpscaleService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UpscaleService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print("Initializing UpscaleService and loading HAT model...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # HAT 모델 인스턴스화 (HAT_SRx4_ImageNet-pretrain.pth에 맞는 아키텍처 파라미터)
        # Real-ESRGANer를 사용하여 모델 로딩 및 추론을 간소화
        # RealESRGANer는 ESRGAN 계열 모델을 로드하는 데 사용되지만,
        # basicsr 라이브러리 내에서 HAT 모델도 유사한 방식으로 처리 가능하도록 설계됨.
        # HAT 모델은 RealESRGANer의 'model' 인자로 직접 전달될 수 있음.
        
        # HAT 모델의 아키텍처 파라미터는 모델 정의에 따라 달라질 수 있습니다.
        # HAT_SRx4_ImageNet-pretrain.pth 모델에 일반적으로 사용되는 파라미터입니다.
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

        self.upsampler = RealESRGANer(
            scale=UPSCALE_SCALE,
            model_path=HAT_MODEL_PATH,
            model=model, # HAT 모델 인스턴스를 직접 전달
            tile=0, # 0으로 설정하면 타일링 사용 안함 (전체 이미지 한 번에 처리)
            tile_pad=10,
            pre_pad=0,
            half=True if self.device == 'cuda' else False,
            model_input_divisible_by=16 # HAT 모델의 window_size에 맞춰 패딩
        )
        print(f"HAT model loaded successfully on {self.device}.")

    async def upscale_image(self, image_bytes: bytes) -> bytes:
        """
        주어진 이미지 바이트를 HAT 모델을 사용하여 업스케일링합니다.
        """
        try:
            # 이미지 바이트를 PIL Image로 변환
            img_pil = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            img_np = np.array(img_pil) # PIL Image를 NumPy 배열로 변환 (HWC, RGB)

            # RealESRGANer는 BGR 포맷을 기대하므로 RGB를 BGR로 변환
            img_np_bgr = img_np[:, :, [2, 1, 0]]

            # 이미지 업스케일링 수행
            # RealESRGANer의 input은 NumPy 배열 (HWC, BGR)
            output_img, _ = self.upsampler.enhance(img_np_bgr, outscale=UPSCALE_SCALE)

            # 결과 이미지는 BGR이므로 다시 RGB로 변환하여 PIL Image로 저장
            output_img_rgb = output_img[:, :, [2, 1, 0]]
            upscaled_pil = Image.fromarray(output_img_rgb)

            # PIL Image를 바이트로 변환
            img_byte_arr = io.BytesIO()
            upscaled_pil.save(img_byte_arr, format='PNG') # PNG 형식으로 저장
            return img_byte_arr.getvalue()

        except Exception as e:
            print(f"Error during image upscaling: {e}")
            raise

# 서비스 인스턴스 생성 (싱글톤)
upscale_service = UpscaleService()
