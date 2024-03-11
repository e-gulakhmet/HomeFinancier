from src.infrastructure.databases import PostgreSQLConnection
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
        str(user.password),
    )
