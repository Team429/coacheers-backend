from fastapi import APIRouter, HTTPException, Depends

from dependencies import get_auth

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)

fake_users_db = {"1": {"name": "박재현"}, "2": {"name": "조유신"}}


@router.get("/")
async def read_items():
    return fake_users_db


@router.get("/me")
async def me(user: str = Depends(get_auth)):
    return user


@router.get("/{user_id}")
async def read_item(user_id: str):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_users_db[user_id]["name"], "user_id": user_id}
