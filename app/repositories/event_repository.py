from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_event_id(self, event_id: str) -> Optional[Event]:
        stmt = select(Event).where(
            Event.event_id == event_id
        )
        return self.db.scalar(stmt)

    def exists(self, event_id: str) -> bool:
        return self.get_by_event_id(event_id) is not None

    def save(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event