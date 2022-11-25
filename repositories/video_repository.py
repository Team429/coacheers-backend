from sqlalchemy.orm import Session
import models
from schemas import video_schema
from services import google_vision


def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()


def create_user_video(db: Session, video: video_schema.VideoCreate):
    db_item = models.Video(**video.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def save_face(db: Session, face: google_vision.Face):
    print(face.joy)


def get_video(db: Session, video_id):
    return db.query(models.Video).filter(models.Video.id == video_id)
