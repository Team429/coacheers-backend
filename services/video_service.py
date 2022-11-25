# input : dir_path, faces, db
# 0. 비디오 row 생성
# 1. 비디오를 만든다
# 2. dir_path와 faces 점수들 가져오기
# 3. db face table 가져오기
# 4. db에 점수들 저장
# output:
from pathlib import Path

from sqlalchemy.orm import Session

import models
from models import Video
from schemas import face_schema
from services.google_vision import Face_DTO


def create_face_rows(faces: list[Face_DTO], video_model: Video, db: Session):
    face_models = []
    for face in faces:
        db_item = models.Face(
            anger_score=face.anger,
            sorrow_score=face.sorrow,
            surprised_score=face.surprise,
            joy_score=face.joy,
            video_id=video_model.id
        )
        face_models.append(db_item)
    db.add_all(face_models)
    db.commit()
    return
