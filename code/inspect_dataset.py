from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"


FILES = [
    "requests.csv",
    "sample_requests.csv",
    "financial_profiles.csv",
    "financial_events.csv",
    "request_payment_options.csv",
    "exchange_rates.csv",
    "messages.csv",
    "images.csv",
]


def inspect_file(filename):
    path = DATASET / filename

    print("\n" + "=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    dataframe = pd.read_csv(path)

    print(f"Rows: {len(dataframe)}")
    print(f"Columns: {len(dataframe.columns)}")

    print("\nCOLUMN NAMES:")
    for column in dataframe.columns:
        print(f"  {column}")

    print("\nDATA TYPES:")
    print(dataframe.dtypes)

    print("\nMISSING VALUES:")
    missing = dataframe.isna().sum()

    if missing.sum() == 0:
        print("  No missing values")
    else:
        print(missing[missing > 0])

    print("\nFIRST 3 ROWS:")
    print(dataframe.head(3).to_string(index=False))


def main():
    print("=" * 80)
    print("BUY OR WAIT - DATASET INSPECTION")
    print("=" * 80)

    for filename in FILES:
        inspect_file(filename)


if __name__ == "__main__":
    main()