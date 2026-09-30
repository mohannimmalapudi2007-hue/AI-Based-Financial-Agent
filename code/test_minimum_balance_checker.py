from minimum_balance_checker import MinimumBalanceChecker


def test_balance_is_safe():
    checker = MinimumBalanceChecker()

    assert checker.is_safe(35000, 30000)


def test_balance_is_not_safe():
    checker = MinimumBalanceChecker()

    assert not checker.is_safe(25000, 30000)


def test_find_lowest_balance():
    checker = MinimumBalanceChecker()

    timeline = [
        {"date": "2025-08-05", "balance_after": 45000},
        {"date": "2025-08-10", "balance_after": 55000},
        {"date": "2025-08-20", "balance_after": 32000},
        {"date": "2025-08-30", "balance_after": 40000},
    ]

    lowest = checker.find_lowest_balance(timeline)

    assert lowest == 32000


def test_empty_timeline():
    checker = MinimumBalanceChecker()

    assert checker.find_lowest_balance([]) is None