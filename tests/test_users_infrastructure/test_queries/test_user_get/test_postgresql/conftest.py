import pytest

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users_infrastructure.queries.user_get import PostgreSQLUserGetQuery


@pytest.fixture()
def user_get_query(postgresql_db: Database[PostgreSQLConnection]) -> PostgreSQLUserGetQuery:
    return PostgreSQLUserGetQuery(db=postgresql_db)
