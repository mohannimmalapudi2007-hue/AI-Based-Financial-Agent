from pathlib import Path

from data_loader import DataLoader
from event_lookup import EventLookup


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def test_event_lookup():
    loader = DataLoader(DATASET)

    events = loader.load_events()

    lookup = EventLookup(events)

    user_events = lookup.get_user_events("user_01")

    assert not user_events.empty
    assert (user_events["user_id"] == "user_01").all()

def test_event_lookup_user_not_found():
    loader = DataLoader(DATASET)

    events = loader.load_events()

    lookup = EventLookup(events)

    user_events = lookup.get_user_events("user_999")

    assert user_events.empty