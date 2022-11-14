from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import face_repository
from schemas import face_schema

router = APIRouter(
    prefix="/faces",
    tags=["face"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=face_schema.Face, summary="표정 생성")
async def create_face(face: face_schema.FaceCreate,
                      db: Session = Depends(get_db)):
    created = face_repository.create_user_face(db, face)
    return created


@router.get("/",response_model=list[face_schema.Face], summary="전체 표정 조회")
async def read_faces(skip:int = 0, limit : int = 400,
                    db:Session = Depends(get_db)):
    faces = face_repository.get_faces(db, skip=skip, limit = limit)
    return faces

@router.get("/{face_id}", response_model=face_schema.Face, summary="단일 표정 조회")
async def read_face(face_id: int, db:Session = Depends(get_db)):
    face = face_repository.get_face(db, face_id)
    return face
