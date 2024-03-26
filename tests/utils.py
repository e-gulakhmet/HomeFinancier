from src.infrastructure.databases import PostgreSQLConnection
from src.storages import Storage
from src.users import User


async def save_user_to_postgresql(db_connection: PostgreSQLConnection, user: User) -> None:
    await db_connection.execute(
        """
        INSERT INTO users (id, created_at, updated_at, email, password_hash)
        VALUES ($1, $2, $3, $4, $5)
        """,
        user.id,
        user.created_at,
        user.updated_at,
        user.email,
        user.password.decode(),
    )


async def save_storage_to_postgresql(db_connection: PostgreSQLConnection, storage: Storage, owner: User) -> None:
    await save_user_to_postgresql(db_connection, owner)

    stmt = """
        INSERT INTO storages (id, created_at, owner_id, link, expenses_table_link, income_table_link)
        VALUES ($1, $2, $3, $4, $5, $6)
    """
    await db_connection.execute(
        stmt,
        storage.id,
        storage.created_at,
        storage.owner_id,
        storage.link,
        storage.expenses_table_link,
        storage.income_table_link,
    )
