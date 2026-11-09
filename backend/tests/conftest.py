"""Pytest configuration for backend tests.

Mocks the database engine before any imports to avoid requiring CockroachDB dialect.
"""

import sys
from unittest import mock


def pytest_configure(config):
    """Configure test environment before collection."""
    # Mock SQLAlchemy engine creation to use SQLite instead of CockroachDB
    with mock.patch("sqlalchemy.create_engine") as mock_create:
        from sqlalchemy import create_engine

        mock_create.side_effect = lambda url, **kwargs: create_engine(
            "sqlite:///:memory:", **kwargs
        )

        # Import constants and patch CONN_STR before any model imports
        import src.constants as constants

        constants.CONN_STR = "sqlite:///:memory:"

    # Now safe to import models - engine will be created with SQLite
    import src.db.main  # noqa: F401


def pytest_collection_modifyitems(config, items):
    """Modify test collection order if needed."""
    pass
