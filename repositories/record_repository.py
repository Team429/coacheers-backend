from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, query

import models
from schemas import record_schema
from repositories import face_repository


def get_recent_records(db: Session, user_id: int):
    return db.query(models.Record).where(models.Record.user_id == user_id).order_by(
        models.Record.created_at).limit(3).all()


def get_record(db: Session, record_id):
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def search_records(user_id, start_date: datetime, db: Session, end_date: datetime = datetime.now()):
    return db.query(models.Record).filter(models.Record.user_id == user_id).filter(
        models.Record.created_at >= start_date).filter(models.Record.created_at <= end_date).all()


def count_records(user_id: int, db: Session):
    return db.query(models.Record).filter(user_id == models.Record.user_id).count()
