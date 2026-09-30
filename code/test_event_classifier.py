from event_classifier import EventClassifier


def test_income_event():
    classifier = EventClassifier()

    event = {
        "direction": "credit"
    }

    assert classifier.is_income(event)
    assert not classifier.is_expense(event)


def test_expense_event():
    classifier = EventClassifier()

    event = {
        "direction": "debit"
    }

    assert classifier.is_expense(event)
    assert not classifier.is_income(event)