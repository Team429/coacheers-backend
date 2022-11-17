from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP)
    length = Column(Integer, default=0)
    size = Column(Integer, default=0)
    record_id = Column(Integer, ForeignKey("records.id"))

    record = relationship("Record", back_populates="video")
    face = relationship("Face", back_populates="video")
    sound = relationship("Sound", back_populates="video")
