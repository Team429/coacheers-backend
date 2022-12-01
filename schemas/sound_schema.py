from datetime import datetime
from pydantic import BaseModel


class SoundBase(BaseModel):
    video_id: int


class SoundCreate(SoundBase):
    high: float
    thick: float
    clean: float
    intensity: float
    stt_content: str
    started_at: datetime
    ended_at: datetime


class Sound(SoundBase):
    id: int

    class Config:
        orm_mode = True
