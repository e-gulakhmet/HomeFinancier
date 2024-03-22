from src.foundation.email import Email
from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User
from src.users_infrastructure.repositories.users import PostgreSQLUsersRepository


async def test_user_exists_returns_true_if_user_exists(
    user: User,
    repository: PostgreSQLUsersRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        await repository.save(user)

        result = await repository.exists(user.email)

    assert result is True


async def test_user_exists_returns_false_if_user_does_not_exist(
    repository: PostgreSQLUsersRepository,
    postgresql_db: Database[PostgreSQLConnection],
) -> None:
    non_existing_email = Email("nonexistent@example.com")
    async with postgresql_db.open_curr_context_connection() as connection, connection.transaction():
        result = await repository.exists(non_existing_email)

    assert result is False
