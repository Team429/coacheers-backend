from pydantic import BaseModel

from schemas import attendance_schema


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    attendances: list[attendance_schema.Attendance] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
