from fastapi import APIRouter
from . import user
from . import item

router = APIRouter()

router.include_router(item.router)
router.include_router(user.router)
