from sqlalchemy.orm import Session
from app import models
from sqlalchemy import desc

def get_latest_survey(db: Session, user_id: int) -> models.Survey | None:
    return (
        db.query(models.Survey)
          .filter(models.Survey.user_id == user_id, models.Survey.completed == True)
          .order_by(desc(models.Survey.id))
          .first()
    )