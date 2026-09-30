from pathlib import Path

from data_loader import DataLoader
from currency_converter import CurrencyConverter


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def test_same_currency():

    loader = DataLoader(DATASET)
    rates = loader.load_exchange_rates()

    converter = CurrencyConverter(rates)

    result = converter.convert(
        100,
        "USD",
        "USD",
        "2023-10-15"
    )

    assert result == 100


def test_currency_conversion():

    loader = DataLoader(DATASET)
    rates = loader.load_exchange_rates()

    converter = CurrencyConverter(rates)

    result = converter.convert(
        100,
        "USD",
        "EUR",
        "2023-10-15"
    )

    assert result == 92


def test_missing_exchange_rate():

    loader = DataLoader(DATASET)
    rates = loader.load_exchange_rates()

    converter = CurrencyConverter(rates)

    try:
        converter.convert(
            100,
            "ABC",
            "EUR",
            "2023-10-15"
        )
        assert False
    except ValueError:
        assert True