from datetime import datetime

from pydantic import BaseModel


class AttendanceBase(BaseModel):
    user_id: int
    created_at: datetime


class AttendanceCreate(AttendanceBase):
    created_at: datetime = datetime.now()
    pass


class AttendanceSearch(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime


class AttendanceSearchMonth(AttendanceSearch):
    start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=000000)


class Attendance(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
