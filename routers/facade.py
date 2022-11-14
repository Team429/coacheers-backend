from fastapi import APIRouter

from . import attendance
from . import user
from . import record
from . import video

router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "Hello from FastAPI!"}


router.include_router(attendance.router)
router.include_router(user.router)
router.include_router(record.router)
router.include_router(video.router)
