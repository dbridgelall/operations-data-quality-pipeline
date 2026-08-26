"""
Database utilities for the Operations Data Quality Pipeline.

This module manages database connections, schema creation, and persistence
of validated operational request records.
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "operations.db"


# ---------------------------------------------------------------------------
# Connection management
# ---------------------------------------------------------------------------

def create_connection(
    database_path: Path = DATABASE_PATH,
) -> sqlite3.Connection:
    """
    Create a connection to the pipeline database.

    Args:
        database_path: Location of the SQLite database.

    Returns:
        Active SQLite database connection.
    """
    database_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(database_path)


# ---------------------------------------------------------------------------
# Schema management
# ---------------------------------------------------------------------------

def create_requests_table(connection: sqlite3.Connection) -> None:
    """
    Create the validated operational requests table when necessary.

    Args:
        connection: Active SQLite database connection.
    """
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS operational_requests (
            request_id TEXT PRIMARY KEY,
            employee_id TEXT NOT NULL,
            department TEXT NOT NULL,
            request_type TEXT NOT NULL,
            submitted_date TEXT NOT NULL,
            completed_date TEXT,
            priority TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    connection.commit()

# ---------------------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------------------

def insert_valid_records(
    connection: sqlite3.Connection,
    data: pd.DataFrame,
) -> None:
    """
    Insert validated operational records into the database.

    Existing request IDs are replaced to keep repeated pipeline runs
    deterministic.

    Args:
        connection: Active SQLite database connection.
        data: Validated operational request records.
    """
    insert_query = """
        INSERT OR REPLACE INTO operational_requests (
            request_id,
            employee_id,
            department,
            request_type,
            submitted_date,
            completed_date,
            priority,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    records = [
        tuple(row)
        for row in data[
            [
                "request_id",
                "employee_id",
                "department",
                "request_type",
                "submitted_date",
                "completed_date",
                "priority",
                "status",
            ]
        ].itertuples(index=False, name=None)
    ]

    connection.executemany(insert_query, records)
    connection.commit()