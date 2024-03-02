from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture

from src.storages import StorageGetQueryProtocol
from src.transactions import (
    Amount,
    Category,
    OwnerID,
    TransactionCreateInput,
    TransactionCreateUseCase,
    TransactionsRepositoryProtocol,
    TransactionType,
)
from src.users import User


@pytest.fixture()
def usecase(mocker: MockerFixture) -> TransactionCreateUseCase:
    return TransactionCreateUseCase(
        storage_get_query=mocker.Mock(spec=StorageGetQueryProtocol),
        transactions_repo=mocker.Mock(spec=TransactionsRepositoryProtocol),
    )


@pytest.fixture()
def input_(user: User) -> TransactionCreateInput:
    return TransactionCreateInput(
        owner_id=OwnerID(user.id),
        type_=TransactionType.EXPENSE,
        amount=Amount(100),
        category=Category("Rent"),
        created_at=datetime.now(tz=timezone.utc),
    )
