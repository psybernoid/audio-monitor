from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .database import Base

class AudioSample(Base):
    __tablename__ = "audio_samples"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    peak_db = Column(Float)


class Audio1Min(Base):
    __tablename__ = "audio_1m"

    minute = Column(DateTime, primary_key=True)
    peak_max = Column(Float)
    peak_avg = Column(Float)
    sample_count = Column(Integer)
