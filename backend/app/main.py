from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="AI Image Upscaler API",
    description="HAT 모델을 사용하여 이미지를 업스케일링하는 API",
    version="1.0.0",
)

# CORS 미들웨어 설정
# 실제 프로덕션 환경에서는 특정 도메인만 허용하도록 변경해야 합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 포함
app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Image Upscaler API!"}
