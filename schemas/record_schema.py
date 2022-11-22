from datetime import datetime, timedelta
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


class RecordSearch(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime


class RecordMonthSearch(RecordSearch):
    start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class RecordWeekSearch(RecordSearch):
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(weeks=1)


class Record(RecordBase):
    id: int
    label: str
    voice_score: float
    face_score: float

    class Config:
        orm_mode = True
