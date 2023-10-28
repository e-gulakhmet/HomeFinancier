import pytest
from pytest_mock import MockerFixture

from src.users.usecases import UserCreateInput, UserCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture, usecase: UserCreateUseCase) -> None:
    mocker.patch.object(usecase, "_validate_email")
    mocker.patch.object(usecase, "_validate_password")


async def test__validate_email_is_called(
        usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_validate_email")

    await usecase._validate(input_)

    spy.assert_called_once_with(email=input_.email)


async def test__validate_password_is_called(
        usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_validate_password")

    await usecase._validate(input_)

    spy.assert_called_once_with(password=input_.password)
