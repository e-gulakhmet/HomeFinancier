from typing import Any

import pytest

from src.infrastructure.databases.base import (
    Database,
    DatabaseConnectionIsNotInitializedError,
    DatabaseIsNotConnectedError,
)


async def test_error_if_database_is_not_connected(database: Database[Any]) -> None:
    with pytest.raises(DatabaseIsNotConnectedError):
        await database.connection


async def test_error_if_connection_is_not_initialized(connected_database: Database[Any]) -> None:
    with pytest.raises(DatabaseConnectionIsNotInitializedError):
        await connected_database.connection


async def test_connection_is_returned_from_context_variable(connected_database: Database[Any]) -> None:
    async with connected_database.open_curr_context_connection():
        assert connected_database.connection is not None
        assert connected_database.connection is connected_database._ctx_var_connection.get()
