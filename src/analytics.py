"""
SQL analytics utilities for operational request data.

This module contains reusable queries that turn validated operational
records into business-level metrics and summaries.
"""

import sqlite3
from typing import Any

import pandas as pd

# ---------------------------------------------------------------------------
# Request metrics
# ---------------------------------------------------------------------------

def get_total_request_count(connection: Any) -> int:
    """
    Return the total number of validated operational requests.

    Args:
        connection: Active database connection.

    Returns:
        Number of records stored in the operational requests table.
    """
    query = """
        SELECT COUNT(*)
        FROM operational_requests
    """

    result = connection.execute(query).fetchone()

    return result[0]


def get_requests_by_department(
    connection: Any,
) -> pd.DataFrame:
    """
    Return request counts grouped by department.

    Args:
        connection: Active database connection.

    Returns:
        Department-level request counts ordered from highest to lowest.
    """
    query = """
        SELECT
            department,
            COUNT(*) AS request_count
        FROM operational_requests
        GROUP BY department
        ORDER BY request_count DESC, department ASC
    """

    return pd.read_sql_query(query, connection)


def get_requests_by_status(
    connection: Any,
) -> pd.DataFrame:
    """
    Return request counts grouped by status.

    Args:
        connection: Active database connection.

    Returns:
        Status-level request counts ordered from highest to lowest.
    """
    query = """
        SELECT
            status,
            COUNT(*) AS request_count
        FROM operational_requests
        GROUP BY status
        ORDER BY request_count DESC, status ASC
    """

    return pd.read_sql_query(query, connection)

# ---------------------------------------------------------------------------
# Processing-time metrics
# ---------------------------------------------------------------------------

def get_average_processing_days(
    connection: Any,
) -> float:
    """
    Return the average completion time for completed requests.

    Uses database-specific SQL where date arithmetic differs between
    SQLite and PostgreSQL.

    Args:
        connection: Active relational database connection.

    Returns:
        Average number of days between submission and completion.
    """
    if isinstance(connection, sqlite3.Connection):
        query = """
            SELECT AVG(
                julianday(completed_date) - julianday(submitted_date)
            )
            FROM operational_requests
            WHERE completed_date IS NOT NULL
        """
    else:
        query = """
            SELECT AVG(
                completed_date::date - submitted_date::date
            )
            FROM operational_requests
            WHERE completed_date IS NOT NULL
        """

    result = connection.execute(query).fetchone()

    if result[0] is None:
        return 0.0

    return round(float(result[0]), 2)

# ---------------------------------------------------------------------------
# Analytics reporting
# ---------------------------------------------------------------------------

def print_analytics_summary(connection: Any) -> None:
    """
    Print key operational metrics generated from SQL queries.

    Args:
        connection: Active database connection.
    """
    total_requests = get_total_request_count(connection)
    average_processing_days = get_average_processing_days(connection)
    department_summary = get_requests_by_department(connection)
    status_summary = get_requests_by_status(connection)

    print("Operational Analytics")
    print("---------------------")
    print(f"Total validated requests: {total_requests}")
    print(f"Average processing time: {average_processing_days} days")
    print()

    print("Requests by Department")
    print(department_summary.to_string(index=False))
    print()

    print("Requests by Status")
    print(status_summary.to_string(index=False))