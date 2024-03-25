from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.users import HashingPortProtocol, UsersRepositoryProtocol, UserVerifyPasswordUseCase


@pytest.fixture()
def users_repository_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=UsersRepositoryProtocol)  # type: ignore


@pytest.fixture()
def hashing_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=HashingPortProtocol)  # type: ignore


@pytest.fixture()
def user_verify_password_usecase(
    users_repository_mock: Mock,
    hashing_mock: Mock,
) -> UserVerifyPasswordUseCase:
    return UserVerifyPasswordUseCase(
        user_repository=users_repository_mock,
        hashing=hashing_mock,
    )
