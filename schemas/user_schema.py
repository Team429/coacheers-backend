from pydantic import BaseModel

from schemas import item_schema


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[item_schema.Item] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
