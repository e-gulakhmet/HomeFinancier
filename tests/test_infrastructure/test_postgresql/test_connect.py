# pyright: reportPrivateUsage=false
import asyncpg
from pytest_mock import MockerFixture

from src.infrastructure.databases.postgresql import PostgreSQL


async def test_asyncpg_create_pool_is_called_to_create_pool(postgresql: PostgreSQL, mocker: MockerFixture) -> None:
    spy = mocker.spy(asyncpg, "create_pool")

    await postgresql.connect()

    spy.assert_called_once_with(
        dsn=postgresql._dsn,
    )
