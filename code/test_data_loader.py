from pathlib import Path

from data_loader import DataLoader


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


def test_data_loader():
    loader = DataLoader(DATASET)

    requests = loader.load_requests()
    profiles = loader.load_profiles()
    events = loader.load_events()

    assert len(requests) == 250
    assert len(profiles) == 275
    assert len(events) == 25342