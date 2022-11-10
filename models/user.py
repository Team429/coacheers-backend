from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(400), unique=True, index=True)
    is_active = Column(Boolean, default=True)

    attendances = relationship("Attendance", back_populates="user")
