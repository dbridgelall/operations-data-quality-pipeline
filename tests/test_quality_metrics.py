"""
Unit tests for dataset-level quality metrics.
"""

import unittest

import pandas as pd

from src.quality_metrics import calculate_quality_metrics


class TestQualityMetrics(unittest.TestCase):
    """Tests for data-quality metric calculations."""

    def setUp(self) -> None:
        """Create reusable sample data and validation results."""
        self.data = pd.DataFrame(
            {
                "request_id": ["REQ-1", "REQ-2", "REQ-3", "REQ-4"],
                "status": ["Completed", "Open", "Open", "Completed"],
            }
        )

        self.quarantined_data = self.data.loc[[1, 2]].copy()

        self.validation_results = {
            "missing_columns": [],
            "missing_required_values": self.data.loc[[1]],
            "invalid_departments": self.data.loc[[2]],
            "invalid_priorities": self.data.loc[[2]],
        }

    def test_calculate_quality_metrics_counts_records(self) -> None:
        """Metrics should report valid and quarantined record counts."""
        result = calculate_quality_metrics(
            self.data,
            self.validation_results,
            self.quarantined_data,
        )

        self.assertEqual(result["total_records"], 4)
        self.assertEqual(result["valid_records"], 2)
        self.assertEqual(result["quarantined_records"], 2)


    def test_calculate_quality_rate(self) -> None:
        """Quality rate should represent the percentage of valid records."""
        result = calculate_quality_metrics(
            self.data,
            self.validation_results,
            self.quarantined_data,
        )

        self.assertEqual(result["quality_rate"], 50.0)

    def test_issue_count_includes_multiple_failures(self) -> None:
        """Issue count should include every detected record-level failure."""
        result = calculate_quality_metrics(
            self.data,
            self.validation_results,
            self.quarantined_data,
        )

        self.assertEqual(result["record_level_issue_count"], 3)

    def test_empty_dataset_returns_zero_quality_rate(self) -> None:
        """An empty dataset should not cause division by zero."""
        empty_data = pd.DataFrame()

        result = calculate_quality_metrics(
            empty_data,
            {},
            empty_data,
        )

        self.assertEqual(result["quality_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()