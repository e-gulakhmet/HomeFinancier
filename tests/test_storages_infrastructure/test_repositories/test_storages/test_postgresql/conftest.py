import pytest
from gspread import Client as GoogleSheetsClient

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages_infrastructure import PostgreSQLGoogleSheetsStoragesRepository


@pytest.fixture()
def repository(
    postgresql_db: Database[PostgreSQLConnection],
    google_sheets_client_mock: GoogleSheetsClient,
) -> PostgreSQLGoogleSheetsStoragesRepository:
    return PostgreSQLGoogleSheetsStoragesRepository(db=postgresql_db, gsc=google_sheets_client_mock)
