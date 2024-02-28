import pytest
from pytest_mock import MockerFixture

from src.users import (
    Email,
    Password,
    UserCreateHashingProviderInterface,
    UserCreateInput,
    UserCreateRepoInterface,
    UserCreateUseCase,
)


@pytest.fixture()
def usecase(mocker: MockerFixture) -> UserCreateUseCase:
    return UserCreateUseCase(
        user_repo=mocker.Mock(spec=UserCreateRepoInterface),
        hashing_provider=mocker.Mock(spec=UserCreateHashingProviderInterface),
    )


@pytest.fixture()
def input_() -> UserCreateInput:
    return UserCreateInput(email=Email("example@example.com"), password=Password("example1234"))
