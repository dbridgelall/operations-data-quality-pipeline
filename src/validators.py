"""
Validation utilities for operational request data.

This module contains reusable validation functions that identify common
data-quality problems without modifying the original dataset.
"""

from collections.abc import Iterable

import pandas as pd


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

VALID_DEPARTMENTS = {
    "IT",
    "HR",
    "Finance",
    "Facilities",
    "Operations",
}

VALID_PRIORITIES = {
    "Low",
    "Medium",
    "High",
}

VALID_STATUSES = {
    "Open",
    "In Progress",
    "Completed",
}

REQUIRED_COLUMNS = {
    "request_id",
    "employee_id",
    "department",
    "request_type",
    "submitted_date",
    "completed_date",
    "priority",
    "status",
}


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def find_missing_columns(
    data: pd.DataFrame,
    required_columns: Iterable[str] = REQUIRED_COLUMNS,
) -> list[str]:
    """
    Return required columns that are missing from the dataset.

    Args:
        data: DataFrame to validate.
        required_columns: Column names required by the pipeline.

    Returns:
        A sorted list of missing column names.
    """
    missing_columns = set(required_columns) - set(data.columns)
    return sorted(missing_columns)


# ---------------------------------------------------------------------------
# Record-level validation
# ---------------------------------------------------------------------------

def find_missing_required_values(
    data: pd.DataFrame,
    required_fields: Iterable[str] = (
        "request_id",
        "employee_id",
        "department",
        "request_type",
        "submitted_date",
        "priority",
        "status",
    ),
) -> pd.DataFrame:
    """
    Return rows containing missing values in required fields.

    completed_date is intentionally excluded because open or in-progress
    requests may not have been completed yet.
    """
    fields = list(required_fields)
    missing_mask = data[fields].isna().any(axis=1)

    return data.loc[missing_mask].copy()


def find_duplicate_request_ids(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return every row whose request_id appears more than once.
    """
    duplicate_mask = data["request_id"].duplicated(keep=False)

    return data.loc[duplicate_mask].copy()


def find_invalid_departments(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return rows containing department values outside the approved list.
    """
    invalid_mask = ~data["department"].isin(VALID_DEPARTMENTS)

    return data.loc[invalid_mask].copy()


def find_invalid_priorities(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return rows containing priority values outside the approved list.
    """
    invalid_mask = ~data["priority"].isin(VALID_PRIORITIES)

    return data.loc[invalid_mask].copy()


def find_invalid_statuses(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return rows containing status values outside the approved list.
    """
    invalid_mask = ~data["status"].isin(VALID_STATUSES)

    return data.loc[invalid_mask].copy()