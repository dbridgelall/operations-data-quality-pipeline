"""
Unit tests for database configuration behavior.
"""

import unittest
from unittest.mock import patch

import src.database as database


class TestDatabaseConfiguration(unittest.TestCase):
    """Tests for database backend selection."""

    def test_default_backend_is_supported(self) -> None:
        """Default configuration should use a supported backend."""
        self.assertIn(
            database.DATABASE_BACKEND,
            {"sqlite", "postgres"},
        )

    @patch("src.database.DATABASE_BACKEND", "unsupported")
    def test_unsupported_backend_raises_error(self) -> None:
        """Unknown database backends should fail explicitly."""
        with self.assertRaises(ValueError):
            database.create_connection()

    @patch("src.database.POSTGRES_PASSWORD", None)
    def test_postgres_requires_password(self) -> None:
        """PostgreSQL should reject missing credentials."""
        with self.assertRaises(ValueError):
            database.create_postgres_connection()


if __name__ == "__main__":
    unittest.main()