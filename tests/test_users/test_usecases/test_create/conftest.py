import pytest
from pytest_mock import MockerFixture

from src.users import Email, HashingPortProtocol, Password, UserCreateInput, UserCreateUseCase, UsersRepositoryProtocol


@pytest.fixture()
def usecase(mocker: MockerFixture) -> UserCreateUseCase:
    return UserCreateUseCase(
        user_repo=mocker.Mock(spec=UsersRepositoryProtocol),
        hashing_provider=mocker.Mock(spec=HashingPortProtocol),
    )


@pytest.fixture()
def input_() -> UserCreateInput:
    return UserCreateInput(email=Email("example@example.com"), password=Password("example1234"))
