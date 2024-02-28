from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture

from src.expenses import (
    Amount,
    Category,
    ExpenseCreateInput,
    ExpenseCreateRepoInterface,
    ExpenseCreateUseCase,
    OwnerID,
)
from src.storages import StorageGetUseCase
from src.users import User


@pytest.fixture()
def usecase(mocker: MockerFixture) -> ExpenseCreateUseCase:
    return ExpenseCreateUseCase(
        storage_get_usecase=mocker.Mock(spec=StorageGetUseCase),
        expense_repo=mocker.Mock(spec=ExpenseCreateRepoInterface),
    )


@pytest.fixture()
def input_(user: User) -> ExpenseCreateInput:
    return ExpenseCreateInput(
        owner_id=OwnerID(user.id),
        amount=Amount(100),
        category=Category("Rent"),
        subcategory="Cleaning",
        created_at=datetime.now(tz=timezone.utc),
    )
