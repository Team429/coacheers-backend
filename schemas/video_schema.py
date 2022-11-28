from datetime import datetime
from pydantic import BaseModel


class VideoBase(BaseModel):
    created_at: datetime
    file_path: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    file_path: str

    class Config:
        orm_mode = True
