"""
Transformation utilities for operational request data.

Transformations standardize values that can be corrected safely without
guessing or changing the underlying meaning of a record.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Normalization mappings
# ---------------------------------------------------------------------------

STATUS_MAPPING = {
    "open": "Open",
    "in progress": "In Progress",
    "completed": "Completed",
    "complete": "Completed",
}


# ---------------------------------------------------------------------------
# Data transformations
# ---------------------------------------------------------------------------

def normalize_statuses(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of the dataset with standardized status values.

    Unknown status values are preserved so validation can flag them later.

    Args:
        data: Operational request dataset.

    Returns:
        A new DataFrame containing normalized status values.
    """
    transformed_data = data.copy()

    normalized_statuses = (
        transformed_data["status"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map(STATUS_MAPPING)
    )

    transformed_data["status"] = normalized_statuses.fillna(
        transformed_data["status"]
    )

    return transformed_data