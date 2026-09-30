from forecast_window import ForecastWindow


def test_get_end_date():
    window = ForecastWindow()

    end_date = window.get_end_date("2025-08-05")

    assert end_date == "2025-11-03"


def test_event_inside_window():
    window = ForecastWindow()

    assert window.is_within_window(
        "2025-09-01",
        "2025-08-05"
    )


def test_event_on_end_date():
    window = ForecastWindow()

    assert window.is_within_window(
        "2025-11-03",
        "2025-08-05"
    )


def test_event_outside_window():
    window = ForecastWindow()

    assert not window.is_within_window(
        "2025-11-04",
        "2025-08-05"
    )