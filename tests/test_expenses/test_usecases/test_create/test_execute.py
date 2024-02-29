# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.expenses import Expense, ExpenseCreateInput, ExpenseCreateUseCase, UserShouldHavePrimaryStorageError
from src.storages import Storage


@pytest.fixture(autouse=True)
def necessary_mocks(
    usecase: ExpenseCreateUseCase,
    mocker: MockerFixture,
    storage: Storage,
) -> None:
    mocker.patch.object(usecase._storage_get_query, "query", return_value=storage)


async def test_error_if_owner_has_no_primary_storage(
    usecase: ExpenseCreateUseCase,
    input_: ExpenseCreateInput,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(usecase._storage_get_query, "query", return_value=None)

    with pytest.raises(UserShouldHavePrimaryStorageError):
        await usecase.execute(input_)


async def test_expense_is_saved_to_repository(
    usecase: ExpenseCreateUseCase,
    input_: ExpenseCreateInput,
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase._expense_repo, "save")
    expected_expense = Expense(
        owner_id=input_.owner_id,
        expenses_storage_link=usecase._storage_get_query.query.return_value.expenses_table_link,  # type: ignore
        amount=input_.amount,
        category=input_.category,
        subcategory=input_.subcategory,
        created_at=input_.created_at,
    )

    await usecase.execute(input_)

    spy.assert_called_once_with(expected_expense)


async def test_expense_entity_is_returned(usecase: ExpenseCreateUseCase, input_: ExpenseCreateInput) -> None:
    storage = await usecase.execute(input_)

    assert isinstance(storage, Expense)
