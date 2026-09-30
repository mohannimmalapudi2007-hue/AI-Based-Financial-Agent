from pathlib import Path

import pandas as pd


class DataLoader:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def load_requests(self):
        path = self.dataset_path / "requests.csv"
        return pd.read_csv(path)

    def load_profiles(self):
        path = self.dataset_path / "financial_profiles.csv"
        return pd.read_csv(path)

    def load_events(self):
        path = self.dataset_path / "financial_events.csv"
        return pd.read_csv(path)

    def load_payment_options(self):
        path = self.dataset_path / "request_payment_options.csv"
        return pd.read_csv(path)

    def load_exchange_rates(self):
        path = self.dataset_path / "exchange_rates.csv"
        return pd.read_csv(path)

    def load_messages(self):
        path = self.dataset_path / "messages.csv"
        return pd.read_csv(path)

    def load_images(self):
        path = self.dataset_path / "images.csv"
        return pd.read_csv(path)