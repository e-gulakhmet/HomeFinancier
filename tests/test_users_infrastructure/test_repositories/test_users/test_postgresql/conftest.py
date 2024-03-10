import pytest

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users_infrastructure import PostgreSQLUsersRepository


@pytest.fixture()
def repository(postgresql_db: Database[PostgreSQLConnection]) -> PostgreSQLUsersRepository:
    return PostgreSQLUsersRepository(postgresql_db)
