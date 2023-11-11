import pytest
from pytest_mock import MockerFixture

from src.expenses.usecases import (
    ExpenseCreateInput,
    ExpenseCreateRepoInterface,
    ExpenseCreateUseCase,
)
from src.storages.usecases import StorageGetUseCase
from src.users.entities import User


@pytest.fixture()
def usecase(mocker: MockerFixture) -> ExpenseCreateUseCase:
    return ExpenseCreateUseCase(
        storage_get_usecase=mocker.Mock(spec=StorageGetUseCase),
        expense_repo=mocker.Mock(spec=ExpenseCreateRepoInterface),
    )


@pytest.fixture()
def input_(user: User) -> ExpenseCreateInput:
    return ExpenseCreateInput(
        user_id=user.id,
        amount=100,
        category="Monthly",
        subcategory="Rent",
    )
