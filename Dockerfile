# 1) 베이스 이미지
FROM python:3.12-slim

# 2) 작업디렉터리
WORKDIR /app

# 3) 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY models/ ./models
COPY train/ ./train

# 5) 포트
EXPOSE 8000

# 6) uvicorn 으로 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--root-path", "/recommend"]