from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, unique=True, index=True)
    filename = Column(String)
    status = Column(String, default="uploaded")
    transcript = Column(Text, nullable=True)
    action_items = Column(JSON, nullable=True)
    decisions = Column(JSON, nullable=True)
    participants = Column(JSON, nullable=True)
    topics = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())