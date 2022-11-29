from sqlalchemy.orm import Session

from models import Video
from repositories import face_repository
from schemas import face_schema
from services.sentiment_analyzing import Face_DTO


def create_faces(faces: list[Face_DTO], video_model: Video, db: Session):
    face_sch_list = list(
        map(lambda f: face_schema.FaceCreate(anger_score=f.anger * 20, joy_score=f.joy * 20,
                                             sorrow_score=f.sorrow * 20,
                                             surprised_score=f.surprise * 20, video_id=video_model.id), faces)
    )
    print(face_sch_list)
    face_repository.create_faces(db, face_sch_list)
