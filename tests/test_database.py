"""
Unit tests for database utilities.

Tests use an in-memory SQLite database so they remain isolated from
development data and do not create persistent test files.
"""

import sqlite3
import unittest

import pandas as pd

from src.database import (
    create_requests_table,
    insert_valid_records,
)


class TestDatabase(unittest.TestCase):
    """Tests for database schema and persistence utilities."""

    def setUp(self) -> None:
        """Create a fresh in-memory database before each test."""
        self.connection = sqlite3.connect(":memory:")

        self.data = pd.DataFrame(
            {
                "request_id": ["REQ-1", "REQ-2"],
                "employee_id": ["EMP-1", "EMP-2"],
                "department": ["IT", "HR"],
                "request_type": ["System Access", "Onboarding"],
                "submitted_date": ["2026-07-01", "2026-07-02"],
                "completed_date": ["2026-07-02", None],
                "priority": ["High", "Medium"],
                "status": ["Completed", "Open"],
            }
        )

    def tearDown(self) -> None:
        """Close the database connection after each test."""
        self.connection.close()

    def test_create_requests_table(self) -> None:
        """Schema creation should create the operational requests table."""
        create_requests_table(self.connection)

        result = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'operational_requests'
            """
        ).fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "operational_requests")

    def test_insert_valid_records(self) -> None:
        """Validated records should be persisted to the database."""
        create_requests_table(self.connection)
        insert_valid_records(self.connection, self.data)

        result = self.connection.execute(
            "SELECT COUNT(*) FROM operational_requests"
        ).fetchone()

        self.assertEqual(result[0], 2)

    def test_repeated_insert_does_not_duplicate_request_ids(self) -> None:
        """Repeated pipeline runs should not create duplicate requests."""
        create_requests_table(self.connection)

        insert_valid_records(self.connection, self.data)
        insert_valid_records(self.connection, self.data)

        result = self.connection.execute(
            "SELECT COUNT(*) FROM operational_requests"
        ).fetchone()

        self.assertEqual(result[0], 2)


if __name__ == "__main__":
    unittest.main()