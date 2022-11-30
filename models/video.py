from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    file_path = Column(String(400))

    face = relationship("Face", back_populates="video")
    sound = relationship("Sound", back_populates="video")
    records = relationship("Record", back_populates="video")
