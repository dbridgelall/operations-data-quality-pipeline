"""
Database utilities for the Operations Data Quality Pipeline.

This module manages database connections, schema creation, and persistence
for supported relational database backends.
"""

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
import psycopg

from src.config import (
    DATABASE_BACKEND,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    SQLITE_DATABASE_PATH,
)


# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "operations.db"

# ---------------------------------------------------------------------------
# Connection management
# ---------------------------------------------------------------------------

def create_sqlite_connection(
    database_path: Path = SQLITE_DATABASE_PATH,
) -> sqlite3.Connection:
    """
    Create a SQLite database connection.

    Args:
        database_path: Location of the SQLite database.

    Returns:
        Active SQLite connection.
    """
    database_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(database_path)


def create_postgres_connection() -> psycopg.Connection:
    """
    Create a PostgreSQL database connection using environment configuration.

    Returns:
        Active PostgreSQL connection.

    Raises:
        ValueError: If the PostgreSQL password is not configured.
    """
    if not POSTGRES_PASSWORD:
        raise ValueError(
            "POSTGRES_PASSWORD must be configured when using PostgreSQL."
        )

    return psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def create_connection() -> Any:
    """
    Create a connection for the configured database backend.

    Returns:
        Active relational database connection.

    Raises:
        ValueError: If DATABASE_BACKEND is unsupported.
    """
    if DATABASE_BACKEND == "sqlite":
        return create_sqlite_connection()

    if DATABASE_BACKEND == "postgres":
        return create_postgres_connection()

    raise ValueError(
        f"Unsupported database backend: {DATABASE_BACKEND}"
    )

# ---------------------------------------------------------------------------
# Schema management
# ---------------------------------------------------------------------------

def create_requests_table(connection: Any) -> None:
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
    connection: Any,
    data: pd.DataFrame,
) -> None:
    """
    Insert validated operational records into the configured database.

    Existing request IDs are updated so repeated pipeline executions remain
    deterministic.

    Args:
        connection: Active relational database connection.
        data: Validated operational request records.
    """
    columns = [
        "request_id",
        "employee_id",
        "department",
        "request_type",
        "submitted_date",
        "completed_date",
        "priority",
        "status",
    ]

    records = [
    tuple(
        None if pd.isna(value) else value
        for value in row
    )
    for row in data[columns].itertuples(
        index=False,
        name=None,
    )
]

    if isinstance(connection, sqlite3.Connection):
        query = """
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

        connection.executemany(query, records)

    else:
        query = """
            INSERT INTO operational_requests (
                request_id,
                employee_id,
                department,
                request_type,
                submitted_date,
                completed_date,
                priority,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (request_id)
            DO UPDATE SET
                employee_id = EXCLUDED.employee_id,
                department = EXCLUDED.department,
                request_type = EXCLUDED.request_type,
                submitted_date = EXCLUDED.submitted_date,
                completed_date = EXCLUDED.completed_date,
                priority = EXCLUDED.priority,
                status = EXCLUDED.status
        """

        with connection.cursor() as cursor:
            cursor.executemany(query, records)

    connection.commit()