"""
Unit tests for processed data output utilities.
"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.writers import write_processed_data


class TestWriters(unittest.TestCase):
    """Tests for processed dataset writers."""

    def setUp(self) -> None:
        """Create reusable valid and quarantined datasets."""
        self.valid_data = pd.DataFrame(
            {
                "request_id": ["REQ-1"],
                "status": ["Completed"],
            }
        )

        self.quarantined_data = pd.DataFrame(
            {
                "request_id": ["REQ-2"],
                "status": ["Open"],
                "quality_issues": ["missing_required_values"],
            }
        )

    def test_write_processed_data_creates_output_files(self) -> None:
        """Valid and quarantined datasets should be written to disk."""
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_path = Path(temp_directory)

            valid_path = temp_path / "valid.csv"
            quarantine_path = temp_path / "quarantine.csv"

            write_processed_data(
                self.valid_data,
                self.quarantined_data,
                valid_path,
                quarantine_path,
            )

            self.assertTrue(valid_path.exists())
            self.assertTrue(quarantine_path.exists())

    def test_written_data_matches_source_data(self) -> None:
        """Written CSV data should preserve the supplied records."""
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_path = Path(temp_directory)

            valid_path = temp_path / "valid.csv"
            quarantine_path = temp_path / "quarantine.csv"

            write_processed_data(
                self.valid_data,
                self.quarantined_data,
                valid_path,
                quarantine_path,
            )

            written_valid_data = pd.read_csv(valid_path)
            written_quarantine_data = pd.read_csv(quarantine_path)

            pd.testing.assert_frame_equal(
                written_valid_data,
                self.valid_data,
            )

            pd.testing.assert_frame_equal(
                written_quarantine_data,
                self.quarantined_data,
            )


if __name__ == "__main__":
    unittest.main()