from datetime import datetime
from pydantic import BaseModel


class SoundBase(BaseModel):
    video_id: int


class SoundCreate(SoundBase):
    db_score: float
    stt_content: str
    frequency_score: float
    started_at: datetime
    ended_at: datetime


class Sound(SoundBase):
    id: int

    class Config:
        orm_mode = True
