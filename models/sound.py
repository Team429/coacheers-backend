from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Float, Text
from sqlalchemy.orm import relationship

from config.database import Base


class Sound(Base):
    __tablename__ = "sounds"

    id = Column(Integer, primary_key=True, index=True)

    high = Column(Float)
    thick = Column(Float)
    clean = Column(Float)
    intensity = Column(Float)

    stt_content = Column(Text, default=None)
    started_at = Column(TIMESTAMP)
    ended_at = Column(TIMESTAMP)

    video_id = Column(Integer, ForeignKey("videos.id"))

    video = relationship("Video", back_populates="sound")
