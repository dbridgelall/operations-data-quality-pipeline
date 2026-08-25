from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "operations_requests.csv"


def load_data(file_path=DATA_PATH):
    """Load operational request data from a CSV file."""
    return pd.read_csv(file_path)


if __name__ == "__main__":
    data = load_data()

    print("Operations Data Quality Pipeline")
    print("--------------------------------")
    print(f"Records loaded: {len(data)}")
    print()
    print(data.head())