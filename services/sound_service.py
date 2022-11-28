import datetime

from sqlalchemy.orm import Session

import models
from models import Sound
from repositories import sound_repository
from schemas import sound_schema


def create_sound(text: str, video: models.Video, db: Session) -> Sound:
    sound_create = sound_schema.SoundCreate(
        frequency_score=0.0,
        db_score=0.0,
        video_id=video.id,
        stt_content=text,
        started_at=datetime.datetime.now(),
        ended_at=datetime.datetime.now(),
        created_at=datetime.datetime.now()
    )
    return sound_repository.create_user_sound(db, sound_create)
