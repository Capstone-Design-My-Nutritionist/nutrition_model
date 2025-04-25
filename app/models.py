from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class FoodLensIntake(Base):
    __tablename__ = "foodlens_intake"

    # PK 및 기본 정보
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    energy_kcal = Column(Float, nullable=True, comment="Energy (kcal)")
    moisture_g = Column(Float, nullable=True, comment="Moisture (g)")
    protein_g = Column(Float, nullable=True, comment="Protein (g)")
    fat_g = Column(Float, nullable=True, comment="Fat (g)")
    carbohydrate_g = Column(Float, nullable=True, comment="Carbohydrate (g)")
    sugar_g = Column(Float, nullable=True, comment="Sugar (g)")
    dietary_fiber_g = Column(Float, nullable=True, comment="Dietary Fiber (g)")
    calcium_mg = Column(Float, nullable=True, comment="Calcium (mg)")
    iron_mg = Column(Float, nullable=True, comment="Iron (mg)")
    sodium_mg = Column(Float, nullable=True, comment="Sodium (mg)")
    vitamin_a_rae_ug = Column(Float, nullable=True, comment="Vitamin A (μg RAE)")
    vitamin_b_rda_ug = Column(Float, nullable=True, comment="Vitamin B (μg RDA)")
    vitamin_c_mg = Column(Float, nullable=True, comment="Vitamin C (mg)")
    vitamin_d_ug = Column(Float, nullable=True, comment="Vitamin D (μg)")
    cholesterol_mg = Column(Float, nullable=True, comment="Cholesterol (mg)")
    saturated_fat_g = Column(Float, nullable=True, comment="Saturated Fat (g)")
    trans_fat_g = Column(Float, nullable=True, comment="Trans Fat (g)")