import datetime

from sqlalchemy.orm import Session

import models
from repositories import video_repository
from schemas import video_schema


def create_video(file_path: str, created_at: datetime.datetime, db: Session) -> models.Video:
    video_sch = video_schema.VideoCreate(created_at=created_at, file_path=file_path)
    created_video = video_repository.create_video(db, video_sch)
    return created_video
