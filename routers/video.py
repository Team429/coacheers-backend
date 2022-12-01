import datetime

import fastapi
from fastapi import APIRouter, Form
from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import video_repository
from schemas import video_schema
from services import sentiment_analyzing, speech_to_text, face_service, video_service, sound_service

router = APIRouter(
    prefix="/videos",
    tags=["video"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", summary="비디오 생성")
async def create_video(video: fastapi.UploadFile, file_path: str = Form(), create_at: datetime.datetime = Form(),
                       db: Session = Depends(get_db)):
    dir_path, faces = await sentiment_analyzing.analyze_video(video)
    text, high, thick, clean, intensity = await speech_to_text.transcript(video)

    created_video = video_service.create_video(file_path, create_at, db)
    sound_service.create_sound(text=text,
                               high=high, thick=thick, clean=clean, intensity=intensity,
                               video=created_video, db=db)
    face_service.create_faces(faces, created_video, db)

    return {"path": dir_path, "face": faces, "video_id": created_video.id}


@router.get("/", response_model=list[video_schema.Video], summary="전체 비디오 조회")
async def read_videos(skip: int = 0, limit: int = 100,
                      db: Session = Depends(get_db)):
    videos = video_repository.get_videos(db, skip=skip, limit=limit)
    return videos


@router.get("/{video_id}", response_model=video_schema.Video, summary="단일 비디오 조회")
async def read_video(video_id: int, db: Session = Depends(get_db)):
    video = video_repository.get_video(db, video_id)
    return video
