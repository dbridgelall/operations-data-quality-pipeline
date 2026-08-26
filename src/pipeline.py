"""
Main entry point for the Operations Data Quality Pipeline.

The pipeline loads raw operational request data, applies safe
transformations, and performs schema and record-level validation.
"""

from pathlib import Path

import pandas as pd

from src.transformers import normalize_statuses
from src.validators import (
    find_duplicate_request_ids,
    find_invalid_date_order,
    find_invalid_dates,
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
        FileNotFoundError: If the supplied CSV file does not exist.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    return pd.read_csv(file_path)


# ---------------------------------------------------------------------------
# Pipeline validation
# ---------------------------------------------------------------------------

def run_validation(data: pd.DataFrame) -> dict[str, object]:
    """
    Run all current validation checks against the supplied dataset.

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
        "invalid_dates": find_invalid_dates(data),
        "invalid_date_order": find_invalid_date_order(data),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_validation_summary(results: dict[str, object]) -> None:
    """
    Print a concise summary of validation findings.

    Args:
        results: Mapping of validation checks to their findings.
    """
    print("Data Quality Summary")
    print("--------------------")

    for check_name, result in results.items():
        issue_count = len(result)

        readable_name = check_name.replace("_", " ").title()
        print(f"{readable_name}: {issue_count}")


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the complete data-quality pipeline."""
    raw_data = load_data()

    # Safely normalize known inconsistencies before validation.
    transformed_data = normalize_statuses(raw_data)

    validation_results = run_validation(transformed_data)

    print("Operations Data Quality Pipeline")
    print("--------------------------------")
    print(f"Records loaded: {len(raw_data)}")
    print()

    print_validation_summary(validation_results)


if __name__ == "__main__":
    main()