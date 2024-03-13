from unittest.mock import Mock

import pytest
from gspread import SpreadsheetNotFound, WorksheetNotFound

from src.transactions import Transaction, TransactionsNoStorageByLinkError
from src.transactions_infrastructure.transactions.googlesheets import GoogleSheetsTransactionsRepository


async def test_error_if_spreadsheet_not_found(
    repository: GoogleSheetsTransactionsRepository,
    google_sheets_client_mock: Mock,
    transaction: Transaction,
) -> None:
    google_sheets_client_mock.open.side_effect = SpreadsheetNotFound

    with pytest.raises(TransactionsNoStorageByLinkError):
        await repository.save(transaction)


async def test_error_if_worksheet_not_found(
    repository: GoogleSheetsTransactionsRepository,
    google_sheets_client_mock: Mock,
    transaction: Transaction,
) -> None:
    google_sheets_client_mock.open.return_value.get_worksheet_by_id.side_effect = WorksheetNotFound

    with pytest.raises(TransactionsNoStorageByLinkError):
        await repository.save(transaction)
