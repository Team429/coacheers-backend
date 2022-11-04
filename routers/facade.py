from fastapi import APIRouter

from . import item
from . import user

router = APIRouter()

router.include_router(item.router)
router.include_router(user.router)
