"""
DB에서 영양 정보 로딩 및 전처리
- nutrition_info 테이블 연결(SQLAlchemy)
- 컬럼명 매핑, 결측치 처리
- 정규화된 deep 입력용 DataFrame (df_nutri_norm)
- 메타 정보 DataFrame (df_meta)
- deep_cols 리스트 반환
"""
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
import os

DB_URL = os.getenv("DB_URL")
ENGINE = create_engine(DB_URL)

deep_cols = [
    'protein_g', 'fat_g', 'carbohydrate_g', 'sugar_g', 'dietary_fiber_g',
    'calcium_mg', 'iron_mg', 'sodium_mg', 'vitamin_a_rae_ug',
    'vitamin_b_rda_mg', 'vitamin_c_mg', 'vitamin_d_ug',
    'cholesterol_mg', 'saturated_fat_g', 'trans_fat_g'
]

def load_and_prepare_from_db(table_name: str = 'food_nutrition'):
    # 1) 테이블에서 전체 로딩
    df = pd.read_sql_table(table_name, con=ENGINE)


    # 3) 결측치 처리
    df[deep_cols] = df[deep_cols].fillna(0)

    # 4) Min-Max 정규화
    scaler = MinMaxScaler()
    norm_vals = scaler.fit_transform(df[deep_cols])
    df_nutri_norm = pd.DataFrame(norm_vals, index=df.index, columns=deep_cols)

    df_meta = df.set_index(df.index)[[
        'food_name', 'rep_food_name', 'serving_size',
        'energy_kcal', 'sodium_mg'
    ]]

    return df_nutri_norm, df_meta, deep_cols
