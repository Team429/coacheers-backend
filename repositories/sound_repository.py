from sqlalchemy.orm import Session
import models
from schemas import sound_schema


def get_sounds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sound).offset(skip).limit(limit).all()


def create_user_sound(db: Session, sound: sound_schema.SoundCreate):
    db_item = models.Sound(**sound.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_sound(db: Session, sound_id):
    return db.query(models.Sound).filter(models.Sound.id == sound_id)
