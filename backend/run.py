import uvicorn
import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
# 이렇게 해야 'app' 모듈을 제대로 임포트할 수 있습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
