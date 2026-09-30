from event_date_handler import EventDateHandler


def test_uses_settlement_date():
    handler = EventDateHandler()

    event = {
        "event_date": "2025-08-10",
        "settlement_date": "2025-08-12"
    }

    result = handler.get_effective_date(event)

    assert result == "2025-08-12"


def test_falls_back_to_event_date():
    handler = EventDateHandler()

    event = {
        "event_date": "2025-08-10",
        "settlement_date": None
    }

    result = handler.get_effective_date(event)

    assert result == "2025-08-10"