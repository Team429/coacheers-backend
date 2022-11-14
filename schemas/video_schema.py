from datetime import datetime
from pydantic import BaseModel


class VideoBase(BaseModel):
    record_id: int
    created_at: datetime


class VideoCreate(VideoBase):
    length: int
    size: int


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True
