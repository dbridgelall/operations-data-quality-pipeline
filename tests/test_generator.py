"""
Unit tests for synthetic operational dataset generation.
"""

import unittest

from src.generator import (
    generate_dataset,
    inject_quality_issues,
)


class TestGenerator(unittest.TestCase):
    """Tests for reproducible synthetic dataset generation."""

    def test_generate_dataset_returns_requested_record_count(self) -> None:
        """Generator should create the requested number of records."""
        result = generate_dataset(record_count=100)

        self.assertEqual(len(result), 100)

    def test_generate_dataset_is_reproducible(self) -> None:
        """Using the same seed should produce identical datasets."""
        first = generate_dataset(record_count=100, seed=42)
        second = generate_dataset(record_count=100, seed=42)

        self.assertTrue(first.equals(second))

    def test_inject_quality_issues_preserves_record_count(self) -> None:
        """Injecting problems should not add or remove records."""
        data = generate_dataset(record_count=100)

        result = inject_quality_issues(data)

        self.assertEqual(len(result), 100)


if __name__ == "__main__":
    unittest.main()