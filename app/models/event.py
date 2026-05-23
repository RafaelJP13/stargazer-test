from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.connection import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(255), unique=True, nullable=False)
    processed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )