# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.exceptions import ValidationError
from src.storages.usecases import StorageCreateInput, StorageCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
    mocker.patch.object(usecase, "_validate_storage_link")
    mocker.patch.object(usecase._user_exist_usecase, "execute", return_value=True)


async def test__validate_storage_link_is_called(
        usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_validate_storage_link")

    await usecase._validate(input_)

    spy.assert_called_once_with(link=input_.link)


class TestCheckingIfUserExists:
    async def test__user_exists_usecase_is_called(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        spy = mocker.spy(usecase._user_exist_usecase, "execute")

        await usecase._validate(input_)

        spy.assert_called_once_with(user_id=input_.user_id)

    async def test_error_if_user_does_not_exist(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._user_exist_usecase, "execute", return_value=False)

        with pytest.raises(ValidationError, match="user_id: User does not exist") as exc:
            await usecase._validate(input_)
        assert exc.value.field == "user_id"
        assert exc.value.error == "User does not exist"

    async def test_no_error_if_user_exists(
            self, usecase: StorageCreateUseCase, input_: StorageCreateInput, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._user_exist_usecase, "execute", return_value=True)

        try:
            await usecase._validate(input_)
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")
