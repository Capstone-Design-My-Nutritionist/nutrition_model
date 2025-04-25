# vectorizer.py
import numpy as np

from app.data_loader import deep_cols

def make_deficiency_vector(survey: dict, foodlens: dict) -> np.ndarray:
    """
    survey: 설문 결과 (예: 키, 몸무게, 섭취 빈도, 선호도 등)
    foodlens: 사진 분석으로 얻은 누적 영양 섭취량
    반환: deep_cols 순서대로 0~1 사이 결핍 벡터
    """
    D = len(deep_cols)
    vec = np.zeros(D)

    # 예시 로직:
    # - survey 내 특정 항목에 따라 결핍 기본값 설정
    # - foodlens로부터 누적 섭취량 계산 후, RDA 대비 비율 결핍도 계산
    #   (더 정확한 로직은 실제 RDA 값표와 연동 필요)

    # 간단히, 모든 요소를 평균값(0.5)로 초기화
    vec.fill(0.5)

    # survey에서 단백질 목표 강조 예시
    if survey.get('concern') == '단백질 결핍':
        idx = deep_cols.index('protein_g')
        vec[idx] = 1.0

    # foodlens 누적 섭취가 많으면 결핍도 낮추기
    for i, col in enumerate(deep_cols):
        intake = foodlens.get(col, 0)
        # 예: 1회 RDA 기준 100% 이상은 결핍도 0
        vec[i] = max(0, 1 - intake)

    return vec