from balance_calculator import BalanceCalculator


def test_apply_expense():
    calculator = BalanceCalculator()

    event = {
        "direction": "debit",
        "amount": 5000
    }

    new_balance = calculator.apply_event(50000, event)

    assert new_balance == 45000


def test_apply_income():
    calculator = BalanceCalculator()

    event = {
        "direction": "credit",
        "amount": 10000
    }

    new_balance = calculator.apply_event(50000, event)

    assert new_balance == 60000


def test_unknown_direction():
    calculator = BalanceCalculator()

    event = {
        "direction": "unknown",
        "amount": 5000
    }

    try:
        calculator.apply_event(50000, event)
        assert False
    except ValueError:
        assert True