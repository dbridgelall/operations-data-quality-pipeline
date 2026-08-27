"""
Application configuration for the Operations Data Quality Pipeline.

Configuration values are read from environment variables so credentials
and environment-specific settings are not stored in source code.
"""

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQLITE_DATABASE_PATH = PROJECT_ROOT / "data" / "operations.db"


# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

DATABASE_BACKEND = os.getenv("DATABASE_BACKEND", "sqlite").lower()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "operations")
POSTGRES_USER = os.getenv("POSTGRES_USER", "operations_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")