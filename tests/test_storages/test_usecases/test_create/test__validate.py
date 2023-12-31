# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.storages.usecases import StorageCreateInput, StorageCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
    mocker.patch.object(usecase, "_validate_storage_link")
    mocker.patch.object(usecase, "_validate_expenses_table_link")
    mocker.patch.object(usecase, "_validate_income_table_link")


async def test__validate_storage_link_is_called(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase, "_validate_storage_link")

    await usecase._validate(input_)

    spy.assert_called_once_with(link=input_.link)


async def test__validate_expenses_table_link_is_called(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase, "_validate_expenses_table_link")

    await usecase._validate(input_)

    spy.assert_called_once_with(link=input_.expenses_table_link)


async def test__validate_income_table_link_is_called(
    usecase: StorageCreateUseCase,
    input_: StorageCreateInput,
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase, "_validate_income_table_link")

    await usecase._validate(input_)

    spy.assert_called_once_with(link=input_.income_table_link)
