from sqlalchemy import Column, ForeignKey, Integer, Float, String, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    anger_score = Column(Integer, default=0)
    joy_score = Column(Integer, default=0)
    sorrow_score = Column(Integer, default=0)
    surprised_score = Column(Integer, default=0)
    voice_score = Column(Float, default=0)

    started_at = Column(TIMESTAMP)
    ended_at = Column(TIMESTAMP)
    video_id = Column(Integer, ForeignKey("videos.id"))

    video = relationship("Video", back_populates="face")

