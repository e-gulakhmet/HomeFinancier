import uuid

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User, UserID
from src.users_infrastructure import PostgreSQLUserGetQuery
from tests.utils import save_user_to_postgresql


async def test_query_returns_correct_user(
    user_get_query: PostgreSQLUserGetQuery,
    user: User,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_user_to_postgresql(connection, user)

        result = await user_get_query.query({"user_id": user.id})

        assert result == user


async def test_query_returns_none_if_user_not_found(
    user_get_query: PostgreSQLUserGetQuery,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        result = await user_get_query.query({"user_id": UserID(uuid.uuid4())})

        assert result is None
