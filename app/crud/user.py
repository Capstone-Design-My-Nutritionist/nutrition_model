from sqlalchemy.orm import Session
from app import models, schemas

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()