from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(400), unique=True, index=True)
    hashed_password = Column(String(400))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
