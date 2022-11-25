from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, query

import models
from schemas import record_schema


def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Record).offset(skip).limit(limit).all()


def create_user_record(db: Session, record: record_schema.RecordCreate):
    db_item = models.Record(**record.dict())
    db_item.face_score = (db_item.anger_score + db_item.surprised_score + db_item.sorrow_score + db_item.joy_score) / 4
    db_item.total_score = (db_item.face_score + db_item.voice_score) / 2
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_record(db: Session, record_id):
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def search_records(user_id, start_date: datetime, db: Session, end_date: datetime = datetime.now()):
    return db.query(models.Record).filter(models.Record.user_id == user_id).filter(
        models.Record.created_at >= start_date).filter(models.Record.created_at <= end_date).all()


def count_records(user_id: int, db: Session):
    return db.query(models.Record).filter(user_id == models.Record.user_id).count()
