import pytest
from pytest_mock import MockerFixture

from src.users.usecases import (
    UserCreateHashingProviderInterface,
    UserCreateInput,
    UserCreateRepoInterface,
    UserCreateUseCase,
    UserCreateUseCaseValidationRules,
)


@pytest.fixture()
def usecase(mocker: MockerFixture) -> UserCreateUseCase:
    return UserCreateUseCase(
        user_repo=mocker.Mock(spec=UserCreateRepoInterface),
        hashing_provider=mocker.Mock(spec=UserCreateHashingProviderInterface),
        validation_rules=UserCreateUseCaseValidationRules(
            password_min_length=4,
        ),
    )


@pytest.fixture()
def input_() -> UserCreateInput:
    return UserCreateInput(
        email="example@email.com",
        password="example_password",
    )
