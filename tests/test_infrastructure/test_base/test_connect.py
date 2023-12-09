from typing import Any

import pytest
from pytest_mock import MockerFixture

from src.infrastructure.databases.base import Database, DatabaseIsAlreadyConnectedError


class TestConnectingToDatabase:
    async def test_error_if_database_is_already_connected(self, connected_database: Database[Any]) -> None:
        with pytest.raises(DatabaseIsAlreadyConnectedError):
            async with connected_database.connect():
                pass

    async def test_engine_connect_is_called_to_connect_to_database(
        self,
        database: Database[Any],
        mocker: MockerFixture,
    ) -> None:
        spy = mocker.spy(database._engine, "connect")

        async with database.connect():
            pass

        spy.assert_called_once()

    async def test_is_connected_is_true_if_database_is_connected(self, database: Database[Any]) -> None:
        assert not database._is_connected

        async with database.connect():
            assert database._is_connected


class TestDisconnectingFromDatabase:
    async def test_engine_disconnect_is_called_to_disconnect_from_database(
        self,
        database: Database[Any],
        mocker: MockerFixture,
    ) -> None:
        spy = mocker.spy(database._engine, "disconnect")

        async with database.connect():
            pass

        spy.assert_called_once()

    async def test_is_connected_is_false_if_database_is_disconnected(self, database: Database[Any]) -> None:
        assert not database._is_connected

        async with database.connect():
            pass

        assert not database._is_connected
