from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import sound_repository
from schemas import sound_schema

router = APIRouter(
    prefix="/sounds",
    tags=["sound"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=sound_schema.Sound, summary="음성 생성")
async def create_sound(sound: sound_schema.SoundCreate,
                       db: Session = Depends(get_db)):
    created = sound_repository.create_user_sound(db, sound)
    return created


@router.get("/", response_model=list[sound_schema.Sound], summary="전체 음성 조회")
async def read_sounds(skip: int = 0, limit: int = 100,
                      db: Session = Depends(get_db)):
    sounds = sound_repository.get_sounds(db, skip=skip, limit=limit)
    return sounds


@router.get("/{sound_id}", response_model=sound_schema.Sound, summary="단일 음성 조회")
async def read_sound(sound_id: int, db: Session = Depends(get_db)):
    sound = sound_repository.get_sound(db, sound_id)
    return sound
