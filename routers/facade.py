from fastapi import APIRouter

from . import item
from . import user

router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "Hello from FastAPI!"}


router.include_router(item.router)
router.include_router(user.router)
