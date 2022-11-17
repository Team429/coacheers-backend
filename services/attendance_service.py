from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from repositories import attendance_repository
from dependencies import get_db
from schemas import attendance_schema


def create_daily_attendance(user_id: int, date: datetime, db: Session = Depends(get_db)):
    exists = attendance_repository.exist_attendance(db, user_id, date)
    if exists:
        raise HTTPException(
            status_code=400,
            detail="Invalid argument",
        )
    else:
        return True


def search_period_attendance(user_id: int, start_date: datetime, db: Session, end_date: datetime = datetime.now()):
    find_attendances = attendance_repository.search_attendances(user_id, start_date, db, end_date)
    return find_attendances
