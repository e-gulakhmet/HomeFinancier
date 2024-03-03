import asyncpg
import pytest
from pytest_mock import MockerFixture

from src.infrastructure.databases.postgresql import (
    Connection,
    PostgreSQL,
    PostgreSQLIsNotConnectedError,
)


async def test_error_if_pool_does_not_exists(postgresql: PostgreSQL, mocker: MockerFixture) -> None:
    connection = mocker.Mock(spec=Connection)

    with pytest.raises(PostgreSQLIsNotConnectedError):
        await postgresql.release(conn=connection)


# It is much more better to test if Pool's release method is called on release.
# But on creating mock or spy for connected_postgresql._pool.release, it raises error:
# AttributeError: Pool object attribute 'release' is read-only.
# So at this moment we only can check, that connection becomes unavailable after release.
async def test_connection_is_unavailable_after_release(
    connected_postgresql: PostgreSQL,
    postgresql_pool_connection: Connection,
) -> None:
    await connected_postgresql.release(conn=postgresql_pool_connection)

    with pytest.raises(asyncpg.exceptions.InterfaceError):
        await postgresql_pool_connection.fetchval("SELECT 1")
