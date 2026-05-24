from datetime import datetime, UTC
from sqlalchemy import Column, DateTime, Integer, String
from app.database.connection import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    event_id = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    processed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
)