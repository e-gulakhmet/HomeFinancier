from typing import Any

import pytest
from pytest_mock import MockerFixture

from src.infrastructure.databases.base import (
    Database,
    DatabaseConnectionIsAlreadyInitializedError,
    DatabaseIsNotConnectedError,
)


class TestCreatingSession:
    async def test_error_if_database_is_not_connected(self, database: Database[Any]) -> None:
        with pytest.raises(DatabaseIsNotConnectedError):
            async with database.open_curr_context_connection():
                pass

    async def test_error_if_session_already_exists_for_current_context(self, connected_database: Database[Any]) -> None:
        async with connected_database.open_curr_context_connection():
            with pytest.raises(DatabaseConnectionIsAlreadyInitializedError):
                async with connected_database.open_curr_context_connection():
                    pass

    async def test_engine_acquire_is_called_to_acquire_session(
        self,
        connected_database: Database[Any],
        mocker: MockerFixture,
    ) -> None:
        spy = mocker.spy(connected_database._engine, "acquire")

        async with connected_database.open_curr_context_connection():
            pass

        spy.assert_called_once()

    async def test_session_is_created_for_current_context(self, connected_database: Database[Any]) -> None:
        async with connected_database.open_curr_context_connection() as session:
            assert session is not None
            assert connected_database._ctx_var_connection.get() is session


class TestClosingSession:
    class TestReleasingSessionUsingEngine:
        async def test_engine_release_is_called_to_release_session(
            self,
            connected_database: Database[Any],
            mocker: MockerFixture,
        ) -> None:
            spy = mocker.spy(connected_database._engine, "release")

            async with connected_database.open_curr_context_connection():
                pass

            spy.assert_called_once()

        async def test_engine_release_is_called_to_release_session_if_error_occurs(
            self,
            connected_database: Database[Any],
            mocker: MockerFixture,
        ) -> None:
            spy = mocker.spy(connected_database._engine, "release")

            try:
                async with connected_database.open_curr_context_connection():
                    raise ValueError  # noqa: TRY301
            except ValueError:
                pass

            spy.assert_called_once()

    class TestRemovingSessionFromCurrentContext:
        async def test_session_is_removed_from_current_context_after_context_is_closed(
            self,
            connected_database: Database[Any],
        ) -> None:
            async with connected_database.open_curr_context_connection():
                pass

            assert connected_database._ctx_var_connection.get(None) is None

        async def test_session_is_removed_from_current_context_if_error_occurs(
            self,
            connected_database: Database[Any],
        ) -> None:
            try:
                async with connected_database.open_curr_context_connection():
                    raise ValueError  # noqa: TRY301
            except ValueError:
                pass

            assert connected_database._ctx_var_connection.get(None) is None
