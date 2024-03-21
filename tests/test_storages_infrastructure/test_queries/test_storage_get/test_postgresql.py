import uuid

import pytest

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages import OwnerID, Storage, StorageID
from src.storages_infrastructure import PostgreSQLStorageGetQuery
from src.users import User
from tests.utils import save_storage_to_postgresql


@pytest.fixture()
def storage_get_query(postgresql_db: Database[PostgreSQLConnection]) -> PostgreSQLStorageGetQuery:
    return PostgreSQLStorageGetQuery(db=postgresql_db)


async def test_query_by_id_returns_storage(
    storage_get_query: PostgreSQLStorageGetQuery,
    storage: Storage,
    user: User,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_storage_to_postgresql(connection, storage=storage, owner=user)

        result = await storage_get_query.query({"id": storage.id})

        assert result is not None
        assert result.id == storage.id


async def test_query_by_owner_id_returns_storage(
    storage_get_query: PostgreSQLStorageGetQuery,
    storage: Storage,
    user: User,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_storage_to_postgresql(connection, storage=storage, owner=user)

        result = await storage_get_query.query({"owner_id": OwnerID(user.id)})

        assert result is not None
        assert result.owner_id == storage.owner_id


async def test_query_with_no_filter_returns_first_storage(
    storage_get_query: PostgreSQLStorageGetQuery,
    postgresql_db: Database[PostgreSQLConnection],
    storage: Storage,
    user: User,
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_storage_to_postgresql(connection, storage=storage, owner=user)

        result = await storage_get_query.query({})

        assert result is not None


async def test_query_by_nonexistent_id_returns_none(
    storage_get_query: PostgreSQLStorageGetQuery,
    postgresql_db: Database[PostgreSQLConnection],
    storage: Storage,
    user: User,
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_storage_to_postgresql(connection, storage=storage, owner=user)
        non_existent_id = StorageID(uuid.uuid4())

        result = await storage_get_query.query({"id": non_existent_id})

        assert result is None


async def test_query_by_nonexistent_owner_id_returns_none(
    storage_get_query: PostgreSQLStorageGetQuery,
    postgresql_db: Database[PostgreSQLConnection],
    storage: Storage,
    user: User,
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_storage_to_postgresql(connection, storage=storage, owner=user)
        non_existent_owner_id = OwnerID(uuid.uuid4())

        result = await storage_get_query.query({"owner_id": non_existent_owner_id})

        assert result is None
