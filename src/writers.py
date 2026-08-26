"""
Output utilities for processed pipeline datasets.

This module handles writing validated and quarantined records to the
processed-data directory.
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

VALID_OUTPUT_PATH = PROCESSED_DATA_DIR / "valid_requests.csv"
QUARANTINE_OUTPUT_PATH = PROCESSED_DATA_DIR / "quarantined_requests.csv"


# ---------------------------------------------------------------------------
# Output utilities
# ---------------------------------------------------------------------------

def write_processed_data(
    valid_data: pd.DataFrame,
    quarantined_data: pd.DataFrame,
    valid_path: Path = VALID_OUTPUT_PATH,
    quarantine_path: Path = QUARANTINE_OUTPUT_PATH,
) -> None:
    """
    Write valid and quarantined records to separate CSV files.

    Parent directories are created automatically when necessary.

    Args:
        valid_data: Records that passed record-level validation.
        quarantined_data: Records that failed one or more validation checks.
        valid_path: Destination for valid records.
        quarantine_path: Destination for quarantined records.
    """
    valid_path.parent.mkdir(parents=True, exist_ok=True)
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)

    valid_data.to_csv(valid_path, index=False)
    quarantined_data.to_csv(quarantine_path, index=False)