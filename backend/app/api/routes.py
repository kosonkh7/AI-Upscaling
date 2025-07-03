from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.services.upscale_service import upscale_service

router = APIRouter()

@router.post("/upscale/")
async def upscale_image_endpoint(file: UploadFile = File(...)):
    """
    이미지 파일을 받아 HAT 모델을 사용하여 업스케일링하고,
    결과 이미지를 직접 반환합니다.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    try:
        image_bytes = await file.read()
        upscaled_image_bytes = await upscale_service.upscale_image(image_bytes)

        # 업스케일된 이미지를 StreamingResponse로 반환
        return StreamingResponse(io.BytesIO(upscaled_image_bytes), media_type="image/png")
    except Exception as e:
        print(f"[ERROR] Upscaling endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"업스케일링 처리 중 오류가 발생했습니다: {str(e)}")
