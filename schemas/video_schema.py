from datetime import datetime
from pydantic import BaseModel


class VideoBase(BaseModel):
    created_at: datetime
    file_path: str


class VideoCreate(VideoBase):
    created_at: datetime = datetime.now()
    file_path: str = "file path"


class Video(VideoBase):
    id: int
    file_path: str

    class Config:
        orm_mode = True
