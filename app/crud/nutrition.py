# app/crud/nutrition.py
from sqlalchemy.orm import Session
from app import models

def get_all_nutrition(db: Session) -> list[models.FoodNutrition]:
    return db.query(models.FoodNutrition).all()

def get_nutrition_by_food(db: Session, food_name: str) -> models.FoodNutrition | None:
    return (
        db.query(models.FoodNutrition)
          .filter(models.FoodNutrition.food_name == food_name)
          .first()
    )