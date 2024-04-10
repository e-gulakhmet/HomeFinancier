from typing import AsyncGenerator

import asyncpg
import pytest

from src.config import Config
from src.infrastructure.databases.postgresql import PostgreSQL, PostgreSQLConnection


@pytest.fixture(scope="session")
def postgresql_dsn(config: Config) -> str:
    return config.test_postgresql_dsn


@pytest.fixture()
def postgresql(postgresql_dsn: str) -> PostgreSQL:
    return PostgreSQL(dsn=postgresql_dsn)


@pytest.fixture()
async def connected_postgresql(postgresql: PostgreSQL) -> AsyncGenerator[PostgreSQL, None]:
    await postgresql.connect()
    try:
        yield postgresql
    finally:
        # Close all Pool's connections
        assert isinstance(postgresql._pool, asyncpg.Pool)  # force check for mypy
        postgresql._pool.terminate()
        await postgresql.disconnect()


@pytest.fixture()
async def postgresql_pool_connection(connected_postgresql: PostgreSQL) -> AsyncGenerator[PostgreSQLConnection, None]:
    connection = await connected_postgresql.acquire()
    try:
        yield connection
    finally:
        await connected_postgresql.release(connection)
