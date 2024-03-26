import uuid

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User, UserID
from src.users_infrastructure import PostgreSQLUsersRepository
from tests.utils import save_user_to_postgresql


async def test_user_is_returned_if_exists(
    repository: PostgreSQLUsersRepository,
    user: User,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_user_to_postgresql(db_connection=postgresql_db.connection, user=user)

        result = await repository.get(filter_={"user_id": user.id})

        assert result == user


async def test_none_is_returned_if_user_does_not_exist(
    repository: PostgreSQLUsersRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        result = await repository.get(filter_={"user_id": UserID(uuid.uuid4())})

        assert result is None


async def test_user_is_found_by_user_id(
    repository: PostgreSQLUsersRepository,
    user: User,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await save_user_to_postgresql(db_connection=postgresql_db.connection, user=user)

        result = await repository.get(filter_={"user_id": user.id})

        assert result == user
