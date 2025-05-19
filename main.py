from fastapi import FastAPI

app = FastAPI(
    docs_url=None,  # 기본 Swagger UI 제거
    openapi_url="/recommend/openapi.json",  # Swagger가 참조할 OpenAPI 경로
    title="Nutrition Recommendation API",
    description="추천 알고리즘을 이용해 개인 맞춤 음식 리스트를 반환합니다.",
    version="1.0.0",
)

# Swagger UI 경로 수동 지정 (/recommend/docs로 접근)
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/recommend/openapi.json",
        title="Nutrition Recommendation API"
    )