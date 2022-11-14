from datetime import datetime
from pydantic import BaseModel


class FaceBase(BaseModel):
    video_id: int


class FaceCreate(FaceBase):
    anger_score: float
    scorn_score: float
    disgust_score: float
    happy_score: float
    neutral_score: float
    sad_score: float
    surprised_score: float
    voice_score: float
    started_at: datetime
    ended_at: datetime


class Face(FaceBase):
    id: int

    class Config:
        orm_mode = True
