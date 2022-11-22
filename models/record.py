from sqlalchemy import Column, ForeignKey, Integer, Float, String, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP)

    label = Column(String(400))
    anger_score = Column(Float)
    scorn_score = Column(Float)
    disgust_score = Column(Float)
    happy_score = Column(Float)
    neutral_score = Column(Float)
    sad_score = Column(Float)
    surprised_score = Column(Float)
    voice_score = Column(Float)
    face_score = Column(Float)

    user = relationship("User", back_populates="records")
    video = relationship("Video", back_populates="record")
