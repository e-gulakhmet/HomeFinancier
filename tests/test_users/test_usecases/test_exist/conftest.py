import pytest
from pytest_mock import MockerFixture

from src.users.usecases import UserExistRepositoryInterface, UserExistUseCase


@pytest.fixture()
def usecase(mocker: MockerFixture) -> UserExistUseCase:
    return UserExistUseCase(
        user_repo=mocker.Mock(spec=UserExistRepositoryInterface),
    )
