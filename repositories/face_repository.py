from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models
from schemas import record_schema
from services import sentiment_analyzing


def get_faces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Face).offset(skip).limit(limit).all()


# def create_user_face(db: Session, face: face_schema.FaceCreate):
#     db_item = models.Face(**face.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

def create_user_face(db: Session, face: sentiment_analyzing.Face_DTO):
    db_item = face.joy + face.anger + face.sorrow + face.surprise
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_face(db: Session, face_id):
    return db.query(models.Face).filter(models.Face.id == face_id)


def get_average_face_score(db: Session, video_id, record: record_schema.RecordCreate):
    anger_score = db.query(func.sum(models.Face.anger_score)).filter(video_id == models.Face.video_id).first()[0]
    joy_score = db.query(func.sum(models.Face.joy_score)).filter(video_id == models.Face.video_id).first()[0]
    sorrow_score = db.query(func.sum(models.Face.sorrow_score)).filter(video_id == models.Face.video_id).first()[0]
    surprised_score = db.query(func.sum(models.Face.surprised_score)).filter(video_id == models.Face.video_id).first()[
        0]
    anger_score = float(anger_score) / db.query(models.Face).filter(video_id == models.Face.video_id).count()
    joy_score = float(joy_score) / db.query(models.Face).filter(video_id == models.Face.video_id).count()
    sorrow_score = float(sorrow_score) / db.query(models.Face).filter(video_id == models.Face.video_id).count()
    surprised_score = float(surprised_score) / db.query(models.Face).filter(video_id == models.Face.video_id).count()

    face_score = float((anger_score + joy_score + sorrow_score + surprised_score) / 4)

    record_models = []
    db_item = models.Record(
        user_id=record.user_id,
        video_id=record.video_id,
        created_at=record.created_at,
        label=record.label,
        filepath=record.filepath,
        voice_score=record.voice_score,
        anger_score=anger_score,
        joy_score=joy_score,
        sorrow_score=sorrow_score,
        surprised_score=surprised_score,
        face_score=face_score,
        total_score=face_score
    )
    record_models.append(db_item)
    db.add_all(record_models)
    db.commit()
    return db_item
