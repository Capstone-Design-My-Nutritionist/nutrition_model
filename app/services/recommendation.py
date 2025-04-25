import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.data_loader import load_and_prepare_from_db

df_nutri_norm, df_meta, deep_cols = load_and_prepare_from_db()

# 하이퍼파라미터
MAX_CAL = 500
MAX_SODIUM = 600
ALPHA, BETA = 0.6, 0.4

def get_recommendations(def_vec: np.ndarray, top_n: int = 5) -> pd.DataFrame:
    X = df_nutri_norm[deep_cols].values
    meta = df_meta[['energy_kcal', 'sodium_mg', 'food_name', 'serving_size']]
    # 2) 원점수 계산
    wsum = X.dot(def_vec)  # (N_foods,)
    cos_sim = cosine_similarity(X, def_vec.reshape(1, -1)).ravel()  # (N_foods,)

    # 3) 0~1 정규화
    wsum_n = (wsum - wsum.min()) / (wsum.max() - wsum.min() + 1e-9)
    cos_n = (cos_sim - cos_sim.min()) / (cos_sim.max() - cos_sim.min() + 1e-9)

    # 4) 기본 점수 (선형 결합)
    base_score = ALPHA * wsum_n + BETA * cos_n  # (N_foods,)

    # 5) 페널티 (칼로리·나트륨 초과 시 0)
    pen_cal = np.clip(1 - meta['energy_kcal'].values / MAX_CAL, 0, 1)
    pen_sod = np.clip(1 - meta['sodium_mg'].values / MAX_SODIUM, 0, 1)
    penalty = pen_cal * pen_sod  # (N_foods,)

    # 6) 최종 스코어
    final_score = base_score * penalty  # (N_foods,)

    # 7) 상위 top_n 인덱스
    idx = np.argsort(-final_score)[:top_n]

    # 8) 결과 DataFrame 구성
    recs = pd.DataFrame({
        'score': final_score[idx],
        'wsum_norm': wsum_n[idx],
        'cos_norm': cos_n[idx],
        'penalty': penalty[idx],
    }, index=df_nutri_norm.index[idx])

    # 9) 메타와 병합
    recs = recs.join(meta, how='left')

    # 10) 반환할 컬럼 순서
    return recs[[
        'food_name', 'serving_size',
        'score', 'wsum_norm', 'cos_norm', 'penalty',
        'energy_kcal', 'sodium_mg'
    ]]