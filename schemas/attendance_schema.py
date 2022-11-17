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


class Attendance(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
