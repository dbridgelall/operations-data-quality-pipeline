"""
Synthetic dataset generator for the Operations Data Quality Pipeline.

This module creates realistic operational request records and intentionally
injects controlled data-quality issues for testing and demonstration.
"""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Generator configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "generated_operations_requests.csv"
)

DEPARTMENTS = [
    "IT",
    "HR",
    "Finance",
    "Facilities",
    "Operations",
]

REQUEST_TYPES = {
    "IT": ["System Access", "Password Reset", "Software Request"],
    "HR": ["Onboarding", "Benefits Request", "Policy Question"],
    "Finance": ["Purchase Request", "Expense Review", "Budget Request"],
    "Facilities": ["Equipment Request", "Maintenance Request", "Room Setup"],
    "Operations": ["Workflow Review", "Process Request", "Access Review"],
}

PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Open", "In Progress", "Completed"]


# ---------------------------------------------------------------------------
# Record generation
# ---------------------------------------------------------------------------

def generate_request_record(
    record_number: int,
    start_date: date,
) -> dict[str, object]:
    """
    Generate one realistic operational request record.

    Args:
        record_number: Sequential number used for record identifiers.
        start_date: Earliest possible request submission date.

    Returns:
        Generated operational request record.
    """
    department = random.choice(DEPARTMENTS)
    submitted_date = start_date + timedelta(
        days=random.randint(0, 180)
    )

    status = random.choice(STATUSES)

    if status == "Completed":
        completed_date = submitted_date + timedelta(
            days=random.randint(0, 10)
        )
    else:
        completed_date = None

    return {
        "request_id": f"REQ-{record_number:06d}",
        "employee_id": f"EMP-{random.randint(1000, 9999)}",
        "department": department,
        "request_type": random.choice(REQUEST_TYPES[department]),
        "submitted_date": submitted_date.isoformat(),
        "completed_date": (
            completed_date.isoformat()
            if completed_date is not None
            else None
        ),
        "priority": random.choice(PRIORITIES),
        "status": status,
    }


def generate_dataset(
    record_count: int = 10_000,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a reproducible synthetic operational dataset.

    Args:
        record_count: Number of operational records to create.
        seed: Random seed used for reproducible generation.

    Returns:
        Generated operational request dataset.
    """
    random.seed(seed)

    start_date = date(2026, 1, 1)

    records = [
        generate_request_record(
            record_number,
            start_date,
        )
        for record_number in range(1, record_count + 1)
    ]

    return pd.DataFrame(records)

# ---------------------------------------------------------------------------
# Data-quality issue injection
# ---------------------------------------------------------------------------

def inject_quality_issues(
    data: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Inject realistic data-quality problems into a copy of the dataset.

    Args:
        data: Clean generated operational data.
        seed: Random seed used for reproducible issue injection.

    Returns:
        Dataset containing controlled quality problems.
    """
    random.seed(seed)

    corrupted_data = data.copy()

    if len(corrupted_data) < 20:
        return corrupted_data

    indexes = list(corrupted_data.index)

    missing_employee_indexes = random.sample(indexes, 20)
    invalid_department_indexes = random.sample(indexes, 20)
    invalid_priority_indexes = random.sample(indexes, 20)
    malformed_date_indexes = random.sample(indexes, 20)
    status_variant_indexes = random.sample(indexes, 20)

    corrupted_data.loc[
        missing_employee_indexes,
        "employee_id",
    ] = None

    corrupted_data.loc[
        invalid_department_indexes,
        "department",
    ] = "Marketing"

    corrupted_data.loc[
        invalid_priority_indexes,
        "priority",
    ] = "Urgent"

    corrupted_data.loc[
        malformed_date_indexes,
        "submitted_date",
    ] = "not-a-date"

    corrupted_data.loc[
        status_variant_indexes,
        "status",
    ] = "OPEN"

    return corrupted_data

# ---------------------------------------------------------------------------
# Dataset persistence
# ---------------------------------------------------------------------------

def write_generated_dataset(
    data: pd.DataFrame,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> None:
    """
    Write generated operational data to disk.

    Args:
        data: Dataset to persist.
        output_path: Destination CSV path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)


def main() -> None:
    """Generate and write a realistic operational dataset."""
    data = generate_dataset()
    corrupted_data = inject_quality_issues(data)

    write_generated_dataset(corrupted_data)

    print("Synthetic Dataset Generator")
    print("---------------------------")
    print(f"Records generated: {len(corrupted_data)}")
    print(f"Output: {DEFAULT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()