from sqlalchemy.orm import Session

import models
import schemas.attendance_schema


def create_user(db: Session, user: schemas.user_schema):
    db_user = models.User(email=user.email, )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User.id).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def exist_user(db: Session, email: str):
    count = db.query(models.User).filter(email == models.User.email).count()
    if count > 0:
        return True
    else:
        return False
