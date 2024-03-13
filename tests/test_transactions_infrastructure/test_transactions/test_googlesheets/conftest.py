from unittest.mock import Mock

import pytest

from src.transactions_infrastructure import GoogleSheetsTransactionsRepository


@pytest.fixture()
def repository(google_sheets_client_mock: Mock) -> GoogleSheetsTransactionsRepository:
    return GoogleSheetsTransactionsRepository(gsc=google_sheets_client_mock)
