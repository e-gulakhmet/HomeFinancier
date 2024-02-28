# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.exceptions.core import ValidationError
from src.storages.entities import Storage
from src.storages.usecases import StorageCreateInput, StorageCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
    mocker.patch.object(usecase._storage_repo, "exists", return_value=False)
    mocker.patch.object(usecase._storage_repo, "is_accessable", return_value=True)


async def test_error_if_storage_link_is_not_accessable(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(usecase._storage_repo, "is_accessable", return_value=False)

    with pytest.raises(ValidationError, match=usecase._STORAGE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT):
        await usecase.execute(input_)


async def test_error_if_expenses_table_link_is_not_accessable(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(usecase._storage_repo, "is_accessable", side_effect=[True, False])

    with pytest.raises(ValidationError, match=usecase._EXPENSES_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT):
        await usecase.execute(input_)


async def test_error_if_income_table_link_is_not_accessable(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(usecase._storage_repo, "is_accessable", side_effect=[True, True, False])

    with pytest.raises(ValidationError, match=usecase._INCOME_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT):
        await usecase.execute(input_)


@pytest.mark.parametrize(
    ("user_has_storages", "primary_flag"),
    [
        (True, False),
        (False, True),
    ],
)
async def test_storage_is_saved_to_repository(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
    user_has_storages: bool,
    primary_flag: bool,
) -> None:
    mocker.patch.object(usecase._storage_repo, "exists", return_value=user_has_storages)
    spy = mocker.spy(usecase._storage_repo, "save")

    await usecase.execute(input_)

    storage = Storage(
        id=mocker.ANY,
        created_at=mocker.ANY,
        primary=primary_flag,
        link=input_.link,
        expenses_table_link=input_.expenses_table_link,
        income_table_link=input_.income_table_link,
        owner_id=input_.owner_id,
    )

    spy.assert_called_once_with(storage=storage)


async def test_domain_is_returned(usecase: StorageCreateUseCase, input_: StorageCreateInput) -> None:
    storage = await usecase.execute(input_)

    assert isinstance(storage, Storage)
