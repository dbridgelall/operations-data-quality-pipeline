"""
Unit tests for operational data transformations.
"""

import unittest

import pandas as pd

from src.transformers import normalize_statuses

class TestTransformers(unittest.TestCase):
    """Tests for reusable data transformation functions."""

    def test_normalize_statuses_standardizes_known_values(self) -> None:
        """Known status variations should use canonical values."""
        data = pd.DataFrame(
            {
                "status": [
                    "OPEN",
                    "open",
                    " complete ",
                    "COMPLETED",
                    "In Progress",
                ]
            }
        )

        result = normalize_statuses(data)

        self.assertEqual(
            result["status"].tolist(),
            [
                "Open",
                "Open",
                "Completed",
                "Completed",
                "In Progress",
            ],
        )

    def test_normalize_statuses_preserves_unknown_values(self) -> None:
        """Unknown values should remain available for later validation."""
        data = pd.DataFrame({"status": ["Waiting"]})

        result = normalize_statuses(data)

        self.assertEqual(result.iloc[0]["status"], "Waiting")

    def test_normalize_statuses_does_not_modify_original_data(self) -> None:
        """Transformations should not mutate the supplied DataFrame."""
        data = pd.DataFrame({"status": ["OPEN"]})

        normalize_statuses(data)

        self.assertEqual(data.iloc[0]["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()