from app.models.event import Event
from app.repositories.event_repository import EventRepository


def test_should_return_true_when_event_already_exists(db):
    repository = EventRepository(db)

    event = Event(
        event_id="evt_existing",
    )

    db.add(event)
    db.commit()

    exists = repository.exists("evt_existing")

    assert exists is True


def test_should_return_false_when_event_does_not_exist(db):
    repository = EventRepository(db)

    exists = repository.exists("evt_missing")

    assert exists is False