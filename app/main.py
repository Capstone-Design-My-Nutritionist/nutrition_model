# app.py
"""
FastAPI 엔드포인트 정의
- 설문 데이터 + 푸드렌즈 데이터 입력 받아
  → 결핍 벡터 생성
  → 추천 결과 반환
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

from app.services.vectorizer import make_deficiency_vector
from app.services.recommendation import get_recommendations

from app.data_loader import ENGINE
import pandas as pd



app = FastAPI(
    title="Nutrition Recommendation API",
    description="추천 알고리즘을 이용해 개인 맞춤 음식 리스트를 반환합니다.",
    version="1.0.0"
)

class RecommendRequest(BaseModel):
    user_id: int
    top_n: int = 5

class RecommendResponseItem(BaseModel):
    food_name: str
    serving_size: str
    score: float
    wsum_norm: float
    cos_norm: float
    penalty: float
    energy_kcal: float
    sodium_mg: float


# app.include_router(user.router,      prefix="/users",      tags=["users"])
# app.include_router(survey.router,    prefix="/survey",     tags=["survey"])
# app.include_router(nutrition.router, prefix="/nutrition",  tags=["nutrition"])
# app.include_router(foodlens.router,  prefix="/foodlens",   tags=["foodlens"])
# app.include_router(meal_log.router,  prefix="/meals",      tags=["meals"])

@app.get("/recommend/{user_id}", response_model=List[RecommendResponseItem])
def recommend_endpoint(user_id: int, top_n: int = 5):
    """
    개인 맞춤 음식 추천
    1) user_id를 통해 설문, 푸드렌즈 데이터를 DB에서 조회
    2) 결핍 벡터 생성$
    3) 추천 알고리즘 실행 후 결과 반환
    """
    survey_sql = ("SELECT * FROM survey"
                  " WHERE user_id = %(uid)s AND completed = TRUE "
                  "ORDER BY id DESC LIMIT 1")
    df_survey = pd.read_sql_query(survey_sql, con=ENGINE, params={"uid": user_id})
    if df_survey.empty:
        raise HTTPException(status_code=404, detail="Completed survey not found for user")
    survey = df_survey.to_dict(orient='records')[0]


    foodLens_sql = ("SELECT nutrient_key, total_amount FROM foodlens_nutrition "
                    "WHERE user_id = :uid")
    df_foodLens = pd.read_sql_query(foodLens_sql, con=ENGINE, params={"uid": user_id})

    foodLens = dict(zip(df_foodLens['nutrient_key'], df_foodLens['total_amount']))

    # 3) 결핍 벡터 생성
    def_vec = make_deficiency_vector(survey, foodLens)

    recs = get_recommendations(np.array(def_vec), top_n=top_n)

    # 5) 결과 직렬화
    result = recs.reset_index()[[
        'food_name', 'serving_size', 'score',
        'wsum_norm', 'cos_norm', 'penalty',
        'energy_kcal', 'sodium_mg'
    ]]

    return result.to_dict(orient="records")