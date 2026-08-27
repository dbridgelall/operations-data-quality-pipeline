"""
Data-quality metric utilities.

This module converts validation findings into high-level metrics that
summarize the health of an operational dataset.
"""

import pandas as pd


def calculate_quality_metrics(
    data: pd.DataFrame,
    validation_results: dict[str, object],
    quarantined_data: pd.DataFrame,
) -> dict[str, float | int]:
    """
    Calculate high-level data-quality metrics.

    Args:
        data: Full transformed dataset.
        validation_results: Validation findings.
        quarantined_data: Records rejected by classification.

    Returns:
        Dictionary containing dataset-level quality metrics.
    """
    total_records = len(data)
    quarantined_records = len(quarantined_data)
    valid_records = total_records - quarantined_records

    quality_rate = (
        (valid_records / total_records) * 100
        if total_records
        else 0.0
    )

    record_level_issue_count = sum(
        len(result)
        for result in validation_results.values()
        if isinstance(result, pd.DataFrame)
    )

    return {
        "total_records": total_records,
        "valid_records": valid_records,
        "quarantined_records": quarantined_records,
        "quality_rate": round(quality_rate, 2),
        "record_level_issue_count": record_level_issue_count,
    }

def print_quality_metrics(
    metrics: dict[str, float | int],
) -> None:
    """
    Print high-level dataset quality metrics.

    Args:
        metrics: Metrics produced by calculate_quality_metrics.
    """
    print("Dataset Quality Metrics")
    print("-----------------------")
    print(f"Total records: {metrics['total_records']:,}")
    print(f"Valid records: {metrics['valid_records']:,}")
    print(
        f"Quarantined records: "
        f"{metrics['quarantined_records']:,}"
    )
    print(f"Quality rate: {metrics['quality_rate']:.2f}%")
    print(
        f"Detected record-level issues: "
        f"{metrics['record_level_issue_count']:,}"
    )