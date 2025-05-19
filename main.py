from fastapi import FastAPI

app = FastAPI(
    docs_url=None,
    openapi_url="/recommend/openapi.json",  # FastAPI가 제공할 openapi.json 경로
    title="Nutrition Recommendation API",
    description="추천 알고리즘을 이용해 개인 맞춤 음식 리스트를 반환합니다.",
    version="1.0.0",
)

@app.get("/recommend/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="./openapi.json",  # 상대 경로로 명시
        title="Nutrition Recommendation API"
    )