from sqlalchemy.orm import Session

from models import Video
from repositories import face_repository
from schemas import face_schema
from services.sentiment_analyzing import Face_DTO


def create_faces(faces: list[Face_DTO], video_model: Video, db: Session):
    face_sch_list = list(
        map(lambda f: face_schema.FaceCreate(anger_score=f.anger, joy_score=f.joy,
                                             sorrow_score=f.sorrow,
                                             surprised_score=f.surprise, video_id=video_model.id), faces)
    )
    face_repository.create_faces(db, face_sch_list)
