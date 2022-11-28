import fastapi
from fastapi import APIRouter

import services.sentiment_analyzing
import services.speech_to_text
from . import attendance
from . import face
from . import record
from . import sound
from . import user
from . import video

router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "Hello from FastAPI!"}


@router.post("/test")
async def test(video: fastapi.UploadFile):
    response1 = await services.speech_to_text.transcript(video, interval=50)
    response2 = await services.sentiment_analyzing.analyze_video(video)
    await video.close()

    return {"msg": "OK", "responses": [response2, response1]}


router.include_router(attendance.router)
router.include_router(user.router)
router.include_router(record.router)
router.include_router(video.router)
router.include_router(face.router)
router.include_router(sound.router)
