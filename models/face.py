from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    anger_score = Column(Integer)
    scorn_score = Column(Integer)
    disgust_score = Column(Integer)
    happy_score = Column(Integer)
    neutral_score = Column(Integer)
    sad_score = Column(Integer)
    surprised_score = Column(Integer)
    voice_score = Column(Integer)

    started_at = Column(TIMESTAMP)
    ended_at = Column(TIMESTAMP)
    video_id = Column(Integer, ForeignKey("videos.id"))

    video = relationship("Video", back_populates="face")
