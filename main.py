from fastapi import FastAPI

app = FastAPI(
    root_path="/recommend",
    docs_url="/docs",
    openapi_url="/openapi.json",
    title="Nutrition Recommendation API",
    description="추천 알고리즘을 이용해 개인 맞춤 음식 리스트를 반환합니다.",
    version="1.0.0"
)