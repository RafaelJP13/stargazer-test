from sqlalchemy.orm import Session
from app.models.event import Event

class EventRepository:

    def __init__(self, db: Session):
        self.db = db

    def exists(
        self,
        event_id: str
    ) -> bool:

        return (
            self.db.query(Event)
            .filter(Event.event_id == event_id)
            .first()
            is not None
        )

    def save(
        self,
        event_id: str
    ) -> Event:

        event = Event(
            event_id=event_id
        )

        self.db.add(event)

        self.db.commit()

        self.db.refresh(event)

        return event