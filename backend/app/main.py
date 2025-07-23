from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api.routes import router
import os

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

# 정적 파일 마운트 (프론트엔드)
# Docker 컨테이너 내의 경로에 맞게 수정됩니다.
# Dockerfile에서 frontend 폴더를 /app/frontend 로 복사할 예정입니다.
static_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
app.mount("/static", StaticFiles(directory=static_files_path), name="static")


@app.get("/")
async def read_root():
    return FileResponse(os.path.join(static_files_path, 'index.html'))
