from sqlalchemy.orm import Session

import models
from schemas import record_schema


def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Record).offset(skip).limit(limit).all()


def create_user_record(db: Session, record: record_schema.RecordCreate):
    db_item = models.Record(**record.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_record(db: Session, record_id):
    return db.query(models.Record).filter(models.Record.id == record_id).first()
