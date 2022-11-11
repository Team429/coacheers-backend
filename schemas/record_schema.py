from datetime import datetime

from pydantic import BaseModel


class RecordBase(BaseModel):
    user_id: int
    created_at: datetime


class RecordCreate(RecordBase):
    label: str
    anger_score: int
    scorn_score: int
    disgust_score: int
    happy_score: int
    neutral_score: int
    sad_score: int
    surprised_score: int
    voice_score: int


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True
