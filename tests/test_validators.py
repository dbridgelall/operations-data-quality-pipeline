"""
Unit tests for data-quality validation functions.
"""

import unittest

import pandas as pd

from src.validators import (
    find_duplicate_request_ids,
    find_invalid_departments,
    find_invalid_priorities,
    find_invalid_statuses,
    find_missing_columns,
    find_missing_required_values,
    find_invalid_date_order,
    find_invalid_dates,
)


class TestValidators(unittest.TestCase):
    """Tests for reusable operational data validators."""

    def setUp(self) -> None:
        """Create a small reusable dataset for each test."""
        self.data = pd.DataFrame(
            {
                "request_id": ["REQ-1", "REQ-2", "REQ-2", "REQ-3"],
                "employee_id": ["EMP-1", None, "EMP-2", "EMP-3"],
                "department": ["IT", "HR", "HR", "Marketing"],
                "request_type": [
                    "System Access",
                    "Onboarding",
                    "Onboarding",
                    "Workflow Review",
                ],
                "submitted_date": [
                    "2026-07-01",
                    "2026-07-02",
                    "2026-07-02",
                    "2026-07-03",
                ],
                "completed_date": [
                    "2026-07-02",
                    None,
                    None,
                    None,
                ],
                "priority": ["High", "Medium", "Medium", "Urgent"],
                "status": ["Completed", "Open", "Open", "OPEN"],
            }
        )

    def test_find_missing_columns_returns_missing_required_columns(self) -> None:
        """Missing schema fields should be reported."""
        incomplete_data = self.data.drop(columns=["priority", "status"])

        result = find_missing_columns(incomplete_data)

        self.assertEqual(result, ["priority", "status"])

    def test_find_missing_columns_returns_empty_list_for_valid_schema(self) -> None:
        """A complete schema should report no missing columns."""
        result = find_missing_columns(self.data)

        self.assertEqual(result, [])

    def test_find_missing_required_values(self) -> None:
        """Rows missing required values should be returned."""
        result = find_missing_required_values(self.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["request_id"], "REQ-2")

    def test_find_duplicate_request_ids(self) -> None:
        """All records sharing a duplicate request ID should be returned."""
        result = find_duplicate_request_ids(self.data)

        self.assertEqual(len(result), 2)
        self.assertTrue((result["request_id"] == "REQ-2").all())

    def test_find_invalid_departments(self) -> None:
        """Unknown departments should be flagged."""
        result = find_invalid_departments(self.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["department"], "Marketing")

    def test_find_invalid_priorities(self) -> None:
        """Unsupported priorities should be flagged."""
        result = find_invalid_priorities(self.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["priority"], "Urgent")

    def test_find_invalid_statuses(self) -> None:
        """Non-standard statuses should be flagged."""
        result = find_invalid_statuses(self.data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["status"], "OPEN")

    def test_find_invalid_dates(self) -> None:
        """Malformed date values should be flagged."""
        data = self.data.copy()
        data.loc[0, "submitted_date"] = "not-a-date"

        result = find_invalid_dates(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["request_id"], "REQ-1")

    def test_find_invalid_date_order(self) -> None:
        """Completion dates before submission dates should be flagged."""
        data = self.data.copy()
        data.loc[0, "submitted_date"] = "2026-07-05"
        data.loc[0, "completed_date"] = "2026-07-02"

        result = find_invalid_date_order(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["request_id"], "REQ-1")

if __name__ == "__main__":
    unittest.main()