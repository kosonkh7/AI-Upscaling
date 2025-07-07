from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import StreamingResponse
import io

from app.services.upscale_service import upscale_service

router = APIRouter()

# 모델 이름을 Form 데이터에서 추출하는 의존성 함수
async def get_model_name(model: str = Form(...)) -> str:
    return model

@router.post("/upscale/")
async def upscale_image_endpoint(file: UploadFile = File(...), model_name: str = Depends(get_model_name)):
    """
    이미지 파일과 모델 이름을 받아 선택된 모델을 사용하여 업스케일링하고,
    결과 이미지를 직접 반환합니다.
    (의존성 주입을 사용하여 모델 이름 처리)
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    try:
        image_bytes = await file.read()
        # 서비스 함수에 모델 이름 전달
        upscaled_image_bytes = await upscale_service.upscale_image(image_bytes, model_name=model_name)

        # 업스케일된 이미지를 StreamingResponse로 반환
        return StreamingResponse(io.BytesIO(upscaled_image_bytes), media_type="image/png")
    except ValueError as e:
        # 잘못된 모델 이름이 전달된 경우
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[ERROR] Upscaling endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"업스케일링 처리 중 오류가 발생했습니다: {str(e)}")
