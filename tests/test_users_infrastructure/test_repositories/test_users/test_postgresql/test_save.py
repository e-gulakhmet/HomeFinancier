from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User
from src.users_infrastructure import PostgreSQLUsersRepository


async def test_user_is_saved_to_db(
    user: User,
    repository: PostgreSQLUsersRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await repository.save(user)

        stmt = "SELECT * FROM users WHERE id = $1"
        result = await postgresql_db.connection.fetchrow(stmt, user.id)
        assert result is not None
        assert dict(result) == {
            "id": user.id,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "email": user.email,
            "password_hash": user.password.decode(),
        }
