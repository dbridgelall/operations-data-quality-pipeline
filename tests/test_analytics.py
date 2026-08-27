"""
Unit tests for SQL analytics utilities.

Tests use an isolated in-memory SQLite database so analytical queries
can be verified without modifying development data.
"""

import sqlite3
import unittest


import pandas as pd

from src.analytics import (
    get_average_processing_days,
    get_requests_by_department,
    get_requests_by_status,
    get_total_request_count,
    query_to_dataframe,
)
from src.database import (
    create_requests_table,
    insert_valid_records,
)


class TestAnalytics(unittest.TestCase):
    """Tests for operational SQL analytics."""

    def setUp(self) -> None:
        """Create and populate an isolated database for each test."""
        self.connection = sqlite3.connect(":memory:")
        create_requests_table(self.connection)

        self.data = pd.DataFrame(
            {
                "request_id": ["REQ-1", "REQ-2", "REQ-3", "REQ-4"],
                "employee_id": ["EMP-1", "EMP-2", "EMP-3", "EMP-4"],
                "department": ["IT", "IT", "HR", "Finance"],
                "request_type": [
                    "System Access",
                    "Password Reset",
                    "Onboarding",
                    "Purchase Request",
                ],
                "submitted_date": [
                    "2026-07-01",
                    "2026-07-02",
                    "2026-07-03",
                    "2026-07-04",
                ],
                "completed_date": [
                    "2026-07-03",
                    "2026-07-03",
                    None,
                    "2026-07-07",
                ],
                "priority": ["High", "Medium", "Medium", "Low"],
                "status": ["Completed", "Completed", "Open", "Completed"],
            }
        )

        insert_valid_records(
            self.connection,
            self.data,
        )

    def tearDown(self) -> None:
        """Close the isolated database after each test."""
        self.connection.close()

    def test_get_total_request_count(self) -> None:
        """Total request count should match stored records."""
        result = get_total_request_count(self.connection)

        self.assertEqual(result, 4)

    def test_get_requests_by_department(self) -> None:
        """Requests should be aggregated by department."""
        result = get_requests_by_department(self.connection)

        it_count = result.loc[
            result["department"] == "IT",
            "request_count",
        ].iloc[0]

        self.assertEqual(it_count, 2)

    def test_get_requests_by_status(self) -> None:
        """Requests should be aggregated by status."""
        result = get_requests_by_status(self.connection)

        completed_count = result.loc[
            result["status"] == "Completed",
            "request_count",
        ].iloc[0]

        self.assertEqual(completed_count, 3)

    def test_get_average_processing_days(self) -> None:
        """Average processing time should use completed requests only."""
        result = get_average_processing_days(self.connection)

        self.assertEqual(result, 2.0)

    def test_query_to_dataframe_returns_query_results(self) -> None:
        """SQL query results should be converted into a labeled DataFrame."""
        result = query_to_dataframe(
            self.connection,
            """
            SELECT request_id, department
            FROM operational_requests
            ORDER BY request_id
            """,
        )

        self.assertEqual(
            result.columns.tolist(),
            ["request_id", "department"],
        )
        self.assertEqual(len(result), 4)
        self.assertEqual(result.iloc[0]["request_id"], "REQ-1")
    
if __name__ == "__main__":
    unittest.main()