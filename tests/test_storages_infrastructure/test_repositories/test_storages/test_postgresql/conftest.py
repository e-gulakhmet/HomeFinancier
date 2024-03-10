import pytest

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages_infrastructure import PostgreSQLStoragesRepository


@pytest.fixture()
def repository(postgresql_db: Database[PostgreSQLConnection]) -> PostgreSQLStoragesRepository:
    return PostgreSQLStoragesRepository(postgresql_db)
