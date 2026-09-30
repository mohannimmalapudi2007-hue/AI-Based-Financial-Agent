from pathlib import Path

from data_loader import DataLoader
from profile_lookup import ProfileLookup


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def test_profile_lookup():
    loader = DataLoader(DATASET)

    profiles = loader.load_profiles()

    lookup = ProfileLookup(profiles)

    profile = lookup.get_profile("user_02")

    assert profile["user_id"] == "user_02"
    assert profile["home_currency"] == "IDR"
    assert profile["current_available_balance"] == 60383889.2
    assert profile["minimum_balance_to_keep"] == 29158400.0


def test_profile_not_found():
    loader = DataLoader(DATASET)

    profiles = loader.load_profiles()

    lookup = ProfileLookup(profiles)

    try:
        lookup.get_profile("user_999")
        assert False
    except ValueError:
        assert True