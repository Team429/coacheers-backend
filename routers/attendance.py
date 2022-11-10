from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import models
from dependencies import get_db
from repositories import attendance_repository
from schemas import attendance_schema

router = APIRouter(
    prefix="/attendances",
    tags=["attendance"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=list[attendance_schema.Attendance], summary="출석 생성")
async def create_attendance(attendance: attendance_schema.AttendanceCreate,
                            db: Session = Depends(get_db)):
    created = attendance_repository.create_user_attendance(db, attendance)
    return created


@router.get("/", response_model=list[attendance_schema.Attendance], summary="출석 전체 조회")
async def read_attendances(skip: int = 0, limit: int = 100,
                           db: Session = Depends(get_db)):
    attendances = attendance_repository.get_attendances(db, skip=skip, limit=limit)
    return attendances


@router.get("/{attendance_id}", response_model=attendance_schema.Attendance, summary="출석 단건 조회")
async def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = attendance_repository.get_attendance(db, attendance_id)
    return attendance
