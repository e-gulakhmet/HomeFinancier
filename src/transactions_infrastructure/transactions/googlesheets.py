from gspread import Client as GoogleSheetsClient
from gspread import SpreadsheetNotFound, WorksheetNotFound

from src.transactions import Transaction, TransactionsNoStorageByLinkError


class GoogleSheetsTransactionsRepository:
    def __init__(self, gsc: GoogleSheetsClient) -> None:
        self._gsc = gsc

    async def save(self, transaction: Transaction) -> None:
        try:
            spreadsheet = self._gsc.open(transaction.storage_link)
        except SpreadsheetNotFound as e:
            raise TransactionsNoStorageByLinkError(transaction.storage_link) from e

        try:
            worksheet = spreadsheet.get_worksheet_by_id(transaction.storage_link)
        except WorksheetNotFound as e:
            raise TransactionsNoStorageByLinkError(transaction.storage_link) from e

        worksheet.append_row(
            (transaction.amount, transaction.category),
        )
