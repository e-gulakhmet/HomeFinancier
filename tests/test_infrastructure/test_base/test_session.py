from typing import Any

import pytest

from src.infrastructure.databases.base import (
    Database,
    DatabaseIsNotConnectedError,
    DatabaseSessionIsNotInitializedError,
)


async def test_error_if_database_is_not_connected(database: Database[Any]) -> None:
    with pytest.raises(DatabaseIsNotConnectedError):
        await database.session


async def test_error_if_session_is_not_initialized(connected_database: Database[Any]) -> None:
    with pytest.raises(DatabaseSessionIsNotInitializedError):
        await connected_database.session


async def test_session_is_returned_from_context_variable(connected_database: Database[Any]) -> None:
    async with connected_database.session_context():
        assert connected_database.session is not None
        assert connected_database.session is connected_database._ctx_var_session.get()
