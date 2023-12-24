from typing import Any, AsyncGenerator

import pytest
from pytest_mock import MockerFixture

from src.infrastructure.databases.base import Database, DatabaseEngineInterface


@pytest.fixture()
def database(mocker: MockerFixture) -> Database[Any]:
    return Database(engine=mocker.Mock(spec=DatabaseEngineInterface))


@pytest.fixture()
async def connected_database(database: Database[Any]) -> AsyncGenerator[Database[Any], None]:
    async with database.connect():
        yield database
