from typing import TYPE_CHECKING, TypeAlias

import asyncpg
from asyncpg import Pool, Record
from asyncpg.pool import PoolConnectionProxy

from src.infrastructure.databases.base import DatabaseEngineInterface

from .exceptions import PostgreSQLIsNotConnectedError

# Prevent runtime error: https://mypy.readthedocs.io/en/stable/runtime_troubles.html?highlight=subscriptable#using-classes-that-are-generic-in-stubs-but-not-at-runtime
if TYPE_CHECKING:
    Connection: TypeAlias = PoolConnectionProxy[Record]
else:
    Connection: TypeAlias = PoolConnectionProxy


class PostgreSQL(DatabaseEngineInterface[Connection]):
    """PostgreSQL database engine"

    Uses asyncpg library to connect to PostgreSQL databases.
    Uses connection pool to prevent creating new connection for each query.
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: Pool[Record] | None = None

    async def connect(self) -> None:
        """Creating connection pool to PostgreSQL database"""
        # Do not check any validation, asyncpg does it by itself
        self._pool = await asyncpg.create_pool(dsn=self._dsn)

    async def disconnect(self) -> None:
        if not self._pool:
            raise PostgreSQLIsNotConnectedError
        await self._pool.close()

    async def acquire(self) -> Connection:
        if not self._pool:
            raise PostgreSQLIsNotConnectedError
        return await self._pool.acquire()

    async def release(self, conn: Connection) -> None:
        if not self._pool:
            raise PostgreSQLIsNotConnectedError
        await self._pool.release(connection=conn)
