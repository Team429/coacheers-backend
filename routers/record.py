from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import models
from dependencies import get_db
from repositories import record_repository
from schemas import record_schema

router = APIRouter(
    prefix="/records",
    tags=["record"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=record_schema.Record, summary="기록 생성")
async def create_record(record: record_schema.RecordCreate,
                        db: Session = Depends(get_db)):
    created = record_repository.create_user_record(db, record)
    return created


@router.get("/", response_model=list[record_schema.Record], summary="기록 전체 조회")
async def read_records(skip: int = 0, limit: int = 100,
                       db: Session = Depends(get_db)):
    records = record_repository.get_records(db, skip=skip, limit=limit)
    return records


@router.get("/{record_id}", response_model=record_schema.Record, summary="기록 단일 조회")
async def read_record(record_id: int, db: Session = Depends(get_db)):
    record = record_repository.get_record(db, record_id)
    return record
