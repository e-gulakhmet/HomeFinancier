import pytest

from src.infrastructure.databases.postgresql import PostgreSQL, PostgreSQLIsNotConnectedError


async def test_error_if_pool_does_not_exists(postgresql: PostgreSQL) -> None:
    with pytest.raises(PostgreSQLIsNotConnectedError):
        await postgresql.acquire()


# It is much more better to test if Pool's acquire method is called on acquire.
# But on creating mock or spy for connected_postgresql._pool.acquire, it raises error:
# AttributeError: Pool object attribute 'acquire' is read-only.
# So at this moment we only can check, that connection becomes available after acquire.
async def test_connection_is_returned(connected_postgresql: PostgreSQL) -> None:
    connection = await connected_postgresql.acquire()

    assert connection is not None
    assert not connection.is_closed()
