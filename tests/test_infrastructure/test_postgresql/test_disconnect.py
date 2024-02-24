import asyncpg

from src.infrastructure.databases.postgresql import PostgreSQL


# It is much more better to test if Pool's close method is called on disconnect.
# But on creating mock or spy for connected_postgresql._pool.close, it raises error:
# AttributeError: Pool object attribute 'close' is read-only.
# So at this moment we only can check, that pool is closed on disconnect.
async def test_pool_is_closed_on_disconnect(connected_postgresql: PostgreSQL) -> None:
    await connected_postgresql.disconnect()

    assert isinstance(connected_postgresql._pool, asyncpg.Pool)  # force check for mypy
    assert connected_postgresql._pool.is_closing() is True
