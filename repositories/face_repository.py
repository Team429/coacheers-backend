from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models
from schemas import record_schema, face_schema
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


def create_faces(db: Session, faces: list[face_schema.FaceCreate]):
    face_models = []
    for face in faces:
        db_item = models.Face(
            anger_score=face.anger_score,
            sorrow_score=face.sorrow_score,
            surprised_score=face.surprised_score,
            joy_score=face.joy_score,
            video_id=face.video_id,
        )
        face_models.append(db_item)
    db.add_all(face_models)
    db.commit()

    return face_models


def get_face(db: Session, face_id):
    return db.query(models.Face).filter(models.Face.id == face_id)


def create_face_record(db: Session, video_id, record: record_schema.RecordCreate):
    anger_score = db.query(func.sum(models.Face.anger_score)).filter(video_id == models.Face.video_id).first()[0]
    joy_score = db.query(func.sum(models.Face.joy_score)).filter(video_id == models.Face.video_id).first()[0]
    sorrow_score = db.query(func.sum(models.Face.sorrow_score)).filter(video_id == models.Face.video_id).first()[0]
    surprised_score = db.query(func.sum(models.Face.surprised_score)).filter(video_id == models.Face.video_id).first()[
        0]
    count = db.query(models.Face).filter(video_id == models.Face.video_id).count()
    anger_score = float(anger_score) / count
    joy_score = float(joy_score) / count
    sorrow_score = float(sorrow_score) / count
    surprised_score = float(surprised_score) / count

    anger_score = float((abs(anger_score - 1) * 10))
    joy_score = float(100 + ((joy_score - 3) * 20))
    sorrow_score = float((abs(sorrow_score - 1) * 5))
    surprised_score = float(abs(surprised_score - 1) * 5)
    if joy_score > 100:
        face_score = joy_score - (joy_score - 100) - anger_score - sorrow_score - surprised_score
    else:
        face_score = joy_score - anger_score - sorrow_score - surprised_score

    high_score = db.query(func.sum(models.Sound.high)).filter(video_id == models.Sound.video_id).first()[0]
    clean_score = db.query(func.sum(models.Sound.clean)).filter(video_id == models.Sound.video_id).first()[0]
    thick_score = db.query(func.sum(models.Sound.thick)).filter(video_id == models.Sound.video_id).first()[0]
    intensity_score = db.query(func.sum(models.Sound.intensity)).filter(video_id == models.Sound.video_id).first()[0]

    voice_score = (high_score * 2 + clean_score + thick_score + intensity_score) / 5

    db_item = models.Record(
        user_id=record.user_id,
        video_id=record.video_id,
        created_at=record.created_at,
        label=record.label,
        filepath=record.filepath,
        voice_score=voice_score,

        anger_score=anger_score,
        joy_score=joy_score,
        sorrow_score=sorrow_score,
        surprised_score=surprised_score,

        high_score=high_score,
        clean_score=clean_score,
        thick_score=thick_score,
        intensity_score=intensity_score,

        face_score=face_score,
        total_score=(face_score + voice_score) / 2
    )
    db.add(db_item)
    db.commit()
    return db_item
