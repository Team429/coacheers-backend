from fastapi import APIRouter, HTTPException, Depends

import models
from dependencies import get_auth, get_db
from repositories import user_repository
from schemas import user_schema
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", summary="신규 유저 생성 및 기존 유저 user_id 반환")
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    if user_repository.exist_user(db, user.email):
        return user_repository.get_user_by_email(db, user.email)
    else:
        created = user_repository.create_user(db, user)
        return created


@router.get("/", response_model=list[user_schema.User])
async def read_items(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db)):
    users = user_repository.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me")
async def me(user: str = Depends(get_auth)):
    return user


@router.get("/{user_id}", response_model=user_schema.User)
async def read_item(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.get_user(db, user_id)
    return user
