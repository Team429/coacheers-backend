from datetime import datetime
from pydantic import BaseModel


class FaceBase(BaseModel):
    video_id: int


class FaceCreate(FaceBase):
    anger_score: int
    joy_score: int
    sorrow_score: int
    surprised_score: int


class Face(FaceBase):
    id: int

    class Config:
        orm_mode = True
