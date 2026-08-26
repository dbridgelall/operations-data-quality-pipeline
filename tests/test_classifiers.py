"""
Unit tests for record classification utilities.
"""

import unittest

import pandas as pd

from src.classifiers import build_issue_map, classify_records


class TestClassifiers(unittest.TestCase):
    """Tests for record-level quality classification."""

    def setUp(self) -> None:
        """Create reusable sample records and validation findings."""
        self.data = pd.DataFrame(
            {
                "request_id": ["REQ-1", "REQ-2", "REQ-3"],
                "employee_id": ["EMP-1", None, "EMP-3"],
                "department": ["IT", "HR", "Marketing"],
            }
        )

        self.validation_results = {
            "missing_columns": [],
            "missing_required_values": self.data.loc[[1]],
            "invalid_departments": self.data.loc[[2]],
        }

    def test_build_issue_map_maps_issues_to_records(self) -> None:
        """Record indexes should map to their corresponding issues."""
        result = build_issue_map(self.validation_results)

        self.assertEqual(
            result,
            {
                1: ["missing_required_values"],
                2: ["invalid_departments"],
            },
        )

    def test_build_issue_map_preserves_multiple_issues(self) -> None:
        """A record failing multiple checks should retain every reason."""
        validation_results = {
            "invalid_departments": self.data.loc[[2]],
            "invalid_priorities": self.data.loc[[2]],
        }

        result = build_issue_map(validation_results)

        self.assertEqual(
            result[2],
            ["invalid_departments", "invalid_priorities"],
        )

    def test_classify_records_separates_valid_records(self) -> None:
        """Records without validation issues should remain valid."""
        valid_data, _ = classify_records(
            self.data,
            self.validation_results,
        )

        self.assertEqual(len(valid_data), 1)
        self.assertEqual(valid_data.iloc[0]["request_id"], "REQ-1")

    def test_classify_records_quarantines_invalid_records(self) -> None:
        """Records with validation issues should be quarantined."""
        _, quarantined_data = classify_records(
            self.data,
            self.validation_results,
        )

        self.assertEqual(len(quarantined_data), 2)

    def test_quarantined_records_include_quality_reasons(self) -> None:
        """Quarantined records should explain why they were rejected."""
        _, quarantined_data = classify_records(
            self.data,
            self.validation_results,
        )

        self.assertIn(
            "quality_issues",
            quarantined_data.columns,
        )

        self.assertEqual(
            quarantined_data.loc[1, "quality_issues"],
            "missing_required_values",
        )


if __name__ == "__main__":
    unittest.main()
