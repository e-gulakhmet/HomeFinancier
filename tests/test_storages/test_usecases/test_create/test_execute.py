# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.storages.entities import Storage
from src.storages.usecases import StorageCreateInput, StorageCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: StorageCreateUseCase, mocker: MockerFixture, storage: Storage) -> None:
    mocker.patch.object(usecase, "_validate")
    mocker.patch.object(usecase, "_create_domain", return_value=storage)


async def test__validate_is_called(
        usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_validate")

    await usecase.execute(input_)

    spy.assert_called_once_with(input_=input_)


async def test_create_domain_entity_is_called(
        usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_create_domain")

    await usecase.execute(input_)

    spy.assert_called_once_with(input_=input_)


class TestSettingPrimaryFlagToStorage:
    async def test__storage_repo_is_called_to_check_if_primary_storage_exists(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        spy = mocker.spy(usecase._storage_repo, "exists")

        await usecase.execute(input_)

        spy.assert_called_once_with(user_id=input_.user_id, primary=True)

    async def test_setting_primary_to_true_if_primary_storage_does_not_exist(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._storage_repo, "exists", return_value=False)

        storage = await usecase.execute(input_)

        assert storage.primary is True

    async def test_setting_primary_to_false_if_primary_storage_exists(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._storage_repo, "exists", return_value=True)

        storage = await usecase.execute(input_)

        assert storage.primary is False


async def test_repo_save_is_called(
        usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase._storage_repo, "save")

    await usecase.execute(input_)


    spy.assert_called_once_with(storage=usecase._create_domain.return_value) # type: ignore


async def test_domain_is_returned(usecase: StorageCreateUseCase, input_: StorageCreateInput) -> None:
    storage = await usecase.execute(input_)

    assert storage == usecase._create_domain.return_value # type: ignore
    assert isinstance(storage, Storage)
