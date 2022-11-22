from datetime import datetime

from sqlalchemy.orm import Session
from repositories import record_repository


def search_period_record(user_id: int, start_date: datetime, db: Session, end_date: datetime = datetime.now()):
    find_records = record_repository.search_records(user_id, start_date, db, end_date)
    return find_records


