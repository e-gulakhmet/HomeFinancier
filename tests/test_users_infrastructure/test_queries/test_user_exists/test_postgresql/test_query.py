from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User
from src.users_infrastructure import PostgreSQLUserExistsQuery
from tests.utils import save_user_to_postgresql


async def test_true_if_user_exists(
    user: User,
    query: PostgreSQLUserExistsQuery,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_user_to_postgresql(postgresql_db.connection, user)

        result = await query.query(user.id)

        assert result is True


async def test_false_if_user_does_not_exists(
    user: User,
    query: PostgreSQLUserExistsQuery,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        result = await query.query(user.id)

        assert result is False
