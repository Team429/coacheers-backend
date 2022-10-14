from fastapi import APIRouter

import item
import user

router = APIRouter()

router.include_router(user.router)
router.include_router(item.router)
