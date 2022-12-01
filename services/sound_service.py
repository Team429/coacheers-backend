import datetime

from sqlalchemy.orm import Session

import models
from models import Sound
from repositories import sound_repository
from schemas import sound_schema


def create_sound(text: str, high, thick, clean, intensity, video: models.Video, db: Session) -> Sound:
    sound_create = sound_schema.SoundCreate(
        high=high,
        thick=thick,
        clean=clean,
        intensity=intensity,
        video_id=video.id,
        stt_content=text,
        started_at=datetime.datetime.now(),
        ended_at=datetime.datetime.now(),
        created_at=datetime.datetime.now()
    )
    return sound_repository.create_user_sound(db, sound_create)
