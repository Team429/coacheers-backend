from fastapi import APIRouter, HTTPException
from dependencies import get_db
from schemas import item_schema
from repositories import item_repository
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(
    prefix="/items",
    tags=["item"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/", response_model=list[item_schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_repository.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
