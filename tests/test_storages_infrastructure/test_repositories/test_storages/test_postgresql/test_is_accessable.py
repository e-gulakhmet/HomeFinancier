from unittest.mock import Mock

import pytest
from gspread import SpreadsheetNotFound

from src.storages import StorageLink
from src.storages_infrastructure import PostgreSQLGoogleSheetsStoragesRepository


@pytest.fixture()
def google_sheets_link() -> StorageLink:
    return StorageLink("https://docs.google.com/spreadsheets/d/1/edit")


async def test_google_sheets_client_is_called_with_link(
    repository: PostgreSQLGoogleSheetsStoragesRepository,
    google_sheets_client_mock: Mock,
) -> None:
    link = StorageLink("https://docs.google.com/spreadsheets/d/1/edit")

    await repository.is_accessable(link)

    google_sheets_client_mock.open_by_url.assert_called_once_with(link)


async def test_false_if_storage_link_is_not_accessable(
    repository: PostgreSQLGoogleSheetsStoragesRepository,
    google_sheets_client_mock: Mock,
) -> None:
    link = StorageLink("https://docs.google.com/spreadsheets/d/1/edit")
    google_sheets_client_mock.open_by_url.side_effect = SpreadsheetNotFound

    result = await repository.is_accessable(link)

    assert result is False


async def test_true_if_storage_link_is_accessable(
    repository: PostgreSQLGoogleSheetsStoragesRepository,
) -> None:
    link = StorageLink("https://docs.google.com/spreadsheets/d/1/edit")

    result = await repository.is_accessable(link)

    assert result is True
