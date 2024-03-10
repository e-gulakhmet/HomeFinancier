from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages import Storage
from src.storages_infrastructure import PostgreSQLStoragesRepository


async def test_storage_is_saved_to_db(
    storage: Storage,
    repository: PostgreSQLStoragesRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await repository.save(storage)

        stmt = "SELECT * FROM storages WHERE id = $1"
        result = await postgresql_db.connection.fetchrow(stmt, storage.id)
        assert result is not None
        assert dict(result) == {
            "id": storage.id,
            "created_at": storage.created_at,
            "link": storage.link,
            "expenses_table_link": storage.expenses_table_link,
            "income_table_link": storage.income_table_link,
            "owner_id": storage.owner_id,
        }
