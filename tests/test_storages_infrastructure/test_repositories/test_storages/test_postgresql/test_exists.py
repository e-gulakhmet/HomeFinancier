from uuid import uuid4

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages import Storage
from src.storages.types import OwnerID
from src.storages_infrastructure import PostgreSQLGoogleSheetsStoragesRepository
from src.users import User
from tests.utils import save_user_to_postgresql


async def test_storage_exists_returns_true_if_storage_exists(
    storage: Storage,
    repository: PostgreSQLGoogleSheetsStoragesRepository,
    postgresql_db: Database[PostgreSQLConnection],
    user: User,
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_user_to_postgresql(connection, user)
        await repository.save(storage)

        result = await repository.exists(storage.owner_id)

    assert result is True


async def test_storage_exists_returns_false_if_storage_does_not_exist(
    repository: PostgreSQLGoogleSheetsStoragesRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    non_existing_owner_id = OwnerID(uuid4())
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        result = await repository.exists(non_existing_owner_id)

    assert result is False
