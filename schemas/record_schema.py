from datetime import datetime

from pydantic import BaseModel


class RecordBase(BaseModel):
    user_id: int
    created_at: datetime


class RecordCreate(RecordBase):
    label: str
    anger_score: float
    scorn_score: float
    disgust_score: float
    happy_score: float
    neutral_score: float
    sad_score: float
    surprised_score: float
    voice_score: float


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True
