"""
Main entry point for the Operations Data Quality Pipeline.

The pipeline currently loads raw operational request data and performs
initial schema and record-level validation.
"""

from pathlib import Path

import pandas as pd

from src.validators import (
    find_duplicate_request_ids,
    find_invalid_departments,
    find_invalid_priorities,
    find_invalid_statuses,
    find_missing_columns,
    find_missing_required_values,
)


# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "operations_requests.csv"


# ---------------------------------------------------------------------------
# Data ingestion
# ---------------------------------------------------------------------------

def load_data(file_path: Path = DATA_PATH) -> pd.DataFrame:
    """
    Load operational request data from a CSV file.

    Args:
        file_path: Path to the raw CSV file.

    Returns:
        Loaded operational data.

    Raises:
        FileNotFoundError: If the supplied CSV does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    return pd.read_csv(file_path)


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def run_validation(data: pd.DataFrame) -> dict[str, object]:
    """
    Run the current set of validation checks.

    Args:
        data: Operational request dataset.

    Returns:
        Mapping of validation categories to their findings.
    """
    return {
        "missing_columns": find_missing_columns(data),
        "missing_required_values": find_missing_required_values(data),
        "duplicate_request_ids": find_duplicate_request_ids(data),
        "invalid_departments": find_invalid_departments(data),
        "invalid_priorities": find_invalid_priorities(data),
        "invalid_statuses": find_invalid_statuses(data),
    }


def print_validation_summary(results: dict[str, object]) -> None:
    """
    Print a concise summary of validation findings.
    """
    print("Data Quality Summary")
    print("--------------------")

    for check_name, result in results.items():
        if isinstance(result, pd.DataFrame):
            issue_count = len(result)
        else:
            issue_count = len(result)

        readable_name = check_name.replace("_", " ").title()
        print(f"{readable_name}: {issue_count}")


def main() -> None:
    """Run the data-quality pipeline."""
    data = load_data()
    validation_results = run_validation(data)

    print("Operations Data Quality Pipeline")
    print("--------------------------------")
    print(f"Records loaded: {len(data)}")
    print()

    print_validation_summary(validation_results)


if __name__ == "__main__":
    main()