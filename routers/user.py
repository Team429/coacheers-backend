from fastapi import APIRouter, HTTPException, Depends

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


@router.post("/", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_repository.create_user(db, user)


@router.get("/", response_model=list[user_schema.User])
async def read_items(skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db)):
    users = user_repository.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me")
async def me(user: str = Depends(get_auth)):
    return user


@router.get("/{user_id}", response_model=user_schema.User)
async def read_item(user_id: int, db:Session = Depends(get_db)):
    user = user_repository.get_user(db, user_id)
    return user