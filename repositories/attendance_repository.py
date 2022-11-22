from datetime import datetime
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


def exist_attendance(db: Session, user_id: int, date: datetime):
    count = db.query(models.Attendance) \
        .filter(models.Attendance.user_id == user_id) \
        .filter(models.Attendance.created_at >= date.today().replace(hour=0, minute=0, second=0, microsecond=0)) \
        .filter(models.Attendance.created_at <= date.today().replace(hour=23, minute=23, second=59, microsecond=999999)) \
        .count()
    if count > 0:
        return True
    else:
        return False


def search_attendances(user_id, start_date: datetime, db: Session, end_date: datetime = datetime.now()):
    return db.query(models.Attendance).filter(models.Attendance.created_at >= start_date).filter(
        models.Attendance.created_at <= end_date).filter(user_id == models.Attendance.user_id).all()
