from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)

    face = relationship("Face", back_populates="video")
    sound = relationship("Sound", back_populates="video")
