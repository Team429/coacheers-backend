from datetime import datetime

from pydantic import BaseModel


class AttendanceBase(BaseModel):
    user_id: int
    created_at: datetime


class AttendanceCreate(AttendanceBase):
    created_at: datetime = datetime.now()
    pass


class Attendance(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
