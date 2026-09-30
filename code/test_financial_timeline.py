from financial_timeline import FinancialTimeline


def test_timeline_uses_only_forecast_events():

    events = [
        {
            "event_id": "event_03",
            "event_date": "2025-12-20",
            "settlement_date": "2025-12-20",
            "amount": 3000,
            "direction": "debit",
        },
        {
            "event_id": "event_01",
            "event_date": "2025-08-05",
            "settlement_date": "2025-08-05",
            "amount": 5000,
            "direction": "debit",
        },
        {
            "event_id": "event_02",
            "event_date": "2025-08-10",
            "settlement_date": "2025-08-10",
            "amount": 10000,
            "direction": "credit",
        },
    ]

    timeline_builder = FinancialTimeline()

    timeline = timeline_builder.build(
        starting_balance=50000,
        start_date="2025-08-05",
        events=events
    )

    assert len(timeline) == 2
    assert timeline[0]["event_id"] == "event_01"
    assert timeline[1]["event_id"] == "event_02"
    assert timeline[0]["balance_after"] == 45000
    assert timeline[1]["balance_after"] == 55000


def test_minimum_balance_is_safe():

    events = [
        {
            "event_id": "event_01",
            "event_date": "2025-08-10",
            "settlement_date": "2025-08-10",
            "amount": 5000,
            "direction": "debit",
        }
    ]

    timeline_builder = FinancialTimeline()

    result = timeline_builder.is_minimum_balance_safe(
        starting_balance=50000,
        start_date="2025-08-05",
        events=events,
        minimum_balance=40000
    )

    assert result


def test_minimum_balance_is_not_safe():

    events = [
        {
            "event_id": "event_01",
            "event_date": "2025-08-10",
            "settlement_date": "2025-08-10",
            "amount": 15000,
            "direction": "debit",
        }
    ]

    timeline_builder = FinancialTimeline()

    result = timeline_builder.is_minimum_balance_safe(
        starting_balance=50000,
        start_date="2025-08-05",
        events=events,
        minimum_balance=40000
    )

    assert not result

def test_timeline_converts_currency():

    class FakeConverter:

        def convert(
            self,
            amount,
            from_currency,
            to_currency,
            rate_date
        ):
            return amount * 2

    events = [
        {
            "event_id": "event_01",
            "event_date": "2025-08-05",
            "settlement_date": "2025-08-05",
            "amount": 100,
            "currency": "USD",
            "direction": "debit",
        }
    ]

    timeline_builder = FinancialTimeline(
        currency_converter=FakeConverter()
    )

    timeline = timeline_builder.build(
        starting_balance=1000,
        start_date="2025-08-05",
        events=events,
        home_currency="EUR"
    )

    assert timeline[0]["amount"] == 200
    assert timeline[0]["balance_after"] == 800


def test_ignores_unknown_status():

    events = [
        {
            "event_id": "event_01",
            "event_date": "2025-08-05",
            "settlement_date": "2025-08-05",
            "amount": 5000,
            "currency": "USD",
            "direction": "debit",
            "status": "cancelled",
        }
    ]

    timeline_builder = FinancialTimeline()

    timeline = timeline_builder.build(
        starting_balance=50000,
        start_date="2025-08-05",
        events=events,
        home_currency="USD"
    )

    assert len(timeline) == 0


def test_keeps_pending_event():

    events = [
        {
            "event_id": "event_01",
            "event_date": "2025-08-05",
            "settlement_date": "2025-08-05",
            "amount": 5000,
            "currency": "USD",
            "direction": "debit",
            "status": "pending",
        }
    ]

    timeline_builder = FinancialTimeline()

    timeline = timeline_builder.build(
        starting_balance=50000,
        start_date="2025-08-05",
        events=events,
        home_currency="USD"
    )

    assert len(timeline) == 1
    assert timeline[0]["status"] == "pending"
    assert timeline[0]["balance_after"] == 45000