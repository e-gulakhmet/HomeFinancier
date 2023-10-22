import pytest
from pytest_mock import MockerFixture

from src.users.entities import User
from src.users.usecases import UserCreateInput, UserCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: UserCreateUseCase, mocker: MockerFixture, user: User) -> None:
    mocker.patch.object(usecase, "_validate")
    mocker.patch.object(usecase, "_create_domain", return_value=user)


async def test__validate_is_called(
        usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_validate")

    await usecase.execute(input_)

    spy.assert_called_once_with(input_=input_)


async def test_create_domain_entity_is_called(
        usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase, "_create_domain")

    await usecase.execute(input_)

    spy.assert_called_once_with(input_=input_)


async def test_repo_save_is_called(
        usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture) -> None:
    spy = mocker.spy(usecase._user_repo, "save")

    await usecase.execute(input_)


    spy.assert_called_once_with(user=usecase._create_domain.return_value) # type: ignore


async def test_domain_is_returned(usecase: UserCreateUseCase, input_: UserCreateInput) -> None:
    user = await usecase.execute(input_)

    assert user == usecase._create_domain.return_value # type: ignore
    assert isinstance(user, User)
