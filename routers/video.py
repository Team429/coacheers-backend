import datetime

import fastapi
from fastapi import APIRouter, Form
from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import video_repository
from schemas import video_schema
from services import video_service
from services.sentiment_analyzing import analyze_video

router = APIRouter(
    prefix="/videos",
    tags=["video"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", summary="비디오 생성")
async def create_video(video: fastapi.UploadFile, file_path: str = Form(), create_at: datetime.datetime = Form(),
                       db: Session = Depends(get_db)):
    dir_path, faces = await analyze_video(video)
    schema = video_schema.VideoCreate()
    schema.created_at = create_at
    schema.file_path = file_path
    created_video = video_repository.create_video(db, schema)
    video_service.create_face_rows(faces, created_video, db)
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
