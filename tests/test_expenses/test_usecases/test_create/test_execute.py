# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.expenses.entities import Expense
from src.expenses.exceptions import UserShouldHavePrimaryStorageError
from src.expenses.usecases import ExpenseCreateInput, ExpenseCreateUseCase
from src.storages.entities import Storage


@pytest.fixture(autouse=True)
def necessary_mocks(
    usecase: ExpenseCreateUseCase,
    mocker: MockerFixture,
    storage: Storage,
    expense: Expense,
) -> None:
    mocker.patch.object(usecase, "_create_domain", return_value=expense)
    mocker.patch.object(usecase._storage_get_usecase, "execute", return_value=storage)


class TestGettingUserPrimaryStorage:
    async def test__storage_get_usecase_is_called_to_get_user_primary_storage(
        self,
        usecase: ExpenseCreateUseCase,
        input_: ExpenseCreateInput,
        mocker: MockerFixture,
    ) -> None:
        spy = mocker.spy(usecase._storage_get_usecase, "execute")

        await usecase.execute(input_)

        spy.assert_called_once_with(filter_={"user_id": input_.user_id, "primary": True})

    async def test_error_if_no_user_primary_storage(
        self,
        usecase: ExpenseCreateUseCase,
        input_: ExpenseCreateInput,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch.object(usecase._storage_get_usecase, "execute", return_value=None)

        with pytest.raises(UserShouldHavePrimaryStorageError):
            await usecase.execute(input_)

    async def test_no_error_if_user_has_primary_storage(
        self,
        usecase: ExpenseCreateUseCase,
        input_: ExpenseCreateInput,
    ) -> None:
        try:
            await usecase.execute(input_)
        except Exception:
            pytest.fail("Unexpected error")


async def test_create_domain_entity_is_called(
    usecase: ExpenseCreateUseCase,
    input_: ExpenseCreateInput,
    mocker: MockerFixture,
    storage: Storage,
) -> None:
    spy = mocker.spy(usecase, "_create_domain")

    await usecase.execute(input_)

    spy.assert_called_once_with(input_=input_, storage=storage)


async def test_repo_save_is_called(
    usecase: ExpenseCreateUseCase,
    input_: ExpenseCreateInput,
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase._expense_repo, "save")

    await usecase.execute(input_)

    spy.assert_called_once_with(expense=usecase._create_domain.return_value)  # type: ignore


async def test_domain_is_returned(usecase: ExpenseCreateUseCase, input_: ExpenseCreateInput) -> None:
    storage = await usecase.execute(input_)

    assert storage == usecase._create_domain.return_value  # type: ignore
    assert isinstance(storage, Expense)
