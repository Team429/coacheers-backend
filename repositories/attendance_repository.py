from sqlalchemy.orm import Session

import models
from schemas import attendance_schema


def get_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendance).offset(skip).limit(limit).all()


def create_user_attendance(db: Session, attendance: attendance_schema.AttendanceCreate):
    db_item = models.Attendance(**attendance.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_attendance(db: Session, attendance_id):
    return db.query(models.Attendance).filter(models.Attendance.id == attendance_id).first()
