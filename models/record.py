from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from config.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP)

    label = Column(String(400),)
    anger_score = Column(Integer)
    scorn_score = Column(Integer)
    disgust_score = Column(Integer)
    happy_score = Column(Integer)
    neutral_score = Column(Integer)
    sad_score = Column(Integer)
    surprised_score = Column(Integer)
    voice_score = Column(Integer)

    user = relationship("User", back_populates="records")
