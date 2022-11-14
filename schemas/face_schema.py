from datetime import datetime
from pydantic import BaseModel


class FaceBase(BaseModel):
    video_id: int


class FaceCreate(FaceBase):
    anger_score: int
    scorn_score: int
    disgust_score: int
    happy_score: int
    neutral_score: int
    sad_score: int
    surprised_score: int
    voice_score: int
    started_at: datetime
    ended_at: datetime


class Face(FaceBase):
    id: int

    class Config:
        orm_mode = True
