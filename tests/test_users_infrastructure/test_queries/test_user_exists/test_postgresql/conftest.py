import pytest

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users_infrastructure import PostgreSQLUserExistsQuery


@pytest.fixture()
def query(postgresql_db: Database[PostgreSQLConnection]) -> PostgreSQLUserExistsQuery:
    return PostgreSQLUserExistsQuery(postgresql_db)
