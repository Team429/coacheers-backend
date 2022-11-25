from sqlalchemy import Column, ForeignKey, Integer, Float, String, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP)

    label = Column(String(400))
    filepath = Column(String(400))

    anger_score = Column(Float, default=0.0)
    scorn_score = Column(Float, default=0.0)
    disgust_score = Column(Float, default=0.0)
    happy_score = Column(Float, default=0.0)
    neutral_score = Column(Float, default=0.0)
    sad_score = Column(Float, default=0.0)
    surprised_score = Column(Float, default=0.0)
    voice_score = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    face_score = Column(Float, default=0.0)

    user = relationship("User", back_populates="records")
    video = relationship("Video", back_populates="record")

