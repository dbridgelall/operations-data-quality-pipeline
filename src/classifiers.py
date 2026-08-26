"""
Record classification utilities for the Operations Data Quality Pipeline.

This module converts validation findings into record-level quality decisions.
Records that fail one or more checks are quarantined with their associated
quality issue reasons.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def build_issue_map(
    validation_results: dict[str, object],
) -> dict[int, list[str]]:
    """
    Map DataFrame row indexes to the validation issues affecting each row.

    Schema-level validation results, such as missing columns, are ignored
    because they apply to the dataset rather than individual records.

    Args:
        validation_results: Mapping of validation names to their findings.

    Returns:
        Mapping of row indexes to one or more validation issue names.
    """
    issue_map: dict[int, list[str]] = {}

    for issue_name, result in validation_results.items():
        if not isinstance(result, pd.DataFrame):
            continue

        for row_index in result.index:
            issue_map.setdefault(row_index, []).append(issue_name)

    return issue_map


def classify_records(
    data: pd.DataFrame,
    validation_results: dict[str, object],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separate valid records from records requiring quarantine.

    Quarantined records receive a quality_issues column containing every
    record-level validation rule they failed.

    Args:
        data: Transformed operational request dataset.
        validation_results: Results produced by the validation framework.

    Returns:
        A tuple containing valid records and quarantined records.
    """
    issue_map = build_issue_map(validation_results)

    quarantine_indexes = list(issue_map.keys())

    valid_data = data.loc[~data.index.isin(quarantine_indexes)].copy()
    quarantined_data = data.loc[data.index.isin(quarantine_indexes)].copy()

    quarantined_data["quality_issues"] = [
        "; ".join(issue_map[row_index])
        for row_index in quarantined_data.index
    ]

    return valid_data, quarantined_data