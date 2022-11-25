from datetime import datetime
from pydantic import BaseModel


class VideoBase(BaseModel):
    created_at: datetime


class VideoCreate(VideoBase):
    created_at: datetime = datetime.now()


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True
