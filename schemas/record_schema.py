from datetime import datetime, timedelta
from pydantic import BaseModel


class RecordBase(BaseModel):
    user_id: int
    created_at: datetime


class RecordCreate(RecordBase):
    label: str
    filepath: str

    anger_score: int
    joy_score: int
    sorrow_score: int
    surprised_score: int

    voice_score: float


class RecordSearch(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime


class RecordMonthSearch(RecordSearch):
    start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


class RecordWeekSearch(RecordSearch):
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(weeks=1)
    end_date = datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=1)


class Record(RecordBase):
    id: int
    label: str
    voice_score: float
    face_score: float
    total_score: float

    class Config:
        orm_mode = True


class RecordOne(BaseModel):
    label: str
    # start_date: datetime
    # end_date: datetime
    voice_score: float
    face_score: float
    total_score: float

    anger_score: int
    joy_score: int
    sorrow_score: int
    surprised_score: int

    class Config:
        orm_mode = True


class RecordSearchTotal(BaseModel):
    user_id: int

    class Config:
        orm_mode = True
