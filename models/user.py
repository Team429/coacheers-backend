from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(400), unique=True, index=True)
    is_active = Column(Boolean, default=True)

    #w자식 객체들을 참조하는 참조 변수
    attendances = relationship("Attendance", back_populates="user")
    records = relationship("Record", back_populates="user")
