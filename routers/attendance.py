from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import models
from dependencies import get_db
from repositories import attendance_repository
from schemas import attendance_schema
from services import attendance_service

router = APIRouter(
    prefix="/attendances",
    tags=["attendance"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=attendance_schema.Attendance, summary="출석 생성")
async def create_attendance(attendance: attendance_schema.AttendanceCreate,
                            db: Session = Depends(get_db)):
    # if attendance_service.create_daily_attendance(attendance.user_id, datetime.now(), db):
    created = attendance_repository.create_user_attendance(db, attendance)
    return created


@router.get("/{attendance_id}", response_model=attendance_schema.Attendance, summary="출석 단건 조회")
async def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = attendance_repository.get_attendance(db, attendance_id)
    return attendance


@router.post("/search", response_model=list[attendance_schema.Attendance], summary="출석 기간 조회")
async def search_period_attendance(attendance: attendance_schema.AttendanceSearch,
                                   db: Session = Depends(get_db)):
    attendance = attendance_service.search_period_attendance(attendance.user_id, attendance.start_date, db,
                                                             datetime.now())
    return attendance


@router.post("/searchmonth", response_model=list[attendance_schema.Attendance], summary="출석 한달 조회")
async def search_month_attendance(attendance: attendance_schema.AttendanceSearchMonth,
                                  db: Session = Depends(get_db)):
    attendance = attendance_service.search_period_attendance(attendance.user_id, attendance.start_date, db,
                                                             datetime.now())
    return attendance
