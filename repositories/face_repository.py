from sqlalchemy.orm import Session
import models
from schemas import face_schema
from services import google_vision


def get_faces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Face).offset(skip).limit(limit).all()


# def create_user_face(db: Session, face: face_schema.FaceCreate):
#     db_item = models.Face(**face.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

def create_user_face(db: Session, face: google_vision.Face_DTO):
    db_item = face.joy + face.anger + face.sorrow + face.surprise
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_face(db: Session, face_id):
    return db.query(models.Face).filter(models.Face.id == face_id)


