from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import models
from dependencies import get_db
from repositories import record_repository, face_repository
from schemas import record_schema
from services import record_service

router = APIRouter(
    prefix="/records",
    tags=["record"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=record_schema.Record, summary="기록 생성")
async def create_record(record: record_schema.RecordCreate,
                        db: Session = Depends(get_db)):
    created = face_repository.get_average_face_score(db, record.video_id, record)
    return created


@router.post("/searchTotal", response_model=list[record_schema.Record], summary="기록 3일 조회")
async def search_total(record: record_schema.RecordSearchTotal, db: Session = Depends(get_db)):
    result = record_repository.get_recent_records(db, record.user_id)
    return result


@router.post("/search", response_model=list[record_schema.Record], summary="기록 기간 조회")
async def search_period_records(record: record_schema.RecordSearch,
                                db: Session = Depends(get_db)):
    record = record_service.search_period_record(record.user_id, record.start_date, db, record.end_date)
    return record


@router.post("/searchmonth", response_model=list[record_schema.Record], summary="기록 한달 조회")
async def search_month_records(record: record_schema.RecordMonthSearch,
                               db: Session = Depends(get_db)):
    record = record_service.search_period_record(record.user_id, record.start_date, db, datetime.now())
    return record


@router.post("/searchweek", response_model=list[record_schema.Record], summary="기록 일주일 조회")
async def search_week_records(record: record_schema.RecordWeekSearch,
                              db: Session = Depends(get_db)):
    record = record_service.search_period_record(record.user_id, record.start_date, db, datetime.now())
    return record


@router.post("/{record_id}", response_model=record_schema.RecordOne, summary="기록 단건 조회")
async def search_record(record_id: int, db: Session = Depends(get_db)):
    record = record_repository.get_record(db, record_id)
    return record
