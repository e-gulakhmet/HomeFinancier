from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from src.auth import AuthConfig, AuthFacade, AuthorizationPortProtocol
from src.users import UserGetQueryProtocol, UserVerifyPasswordUseCase


@pytest.fixture()
def user_get_query_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=UserGetQueryProtocol)  # type: ignore


@pytest.fixture()
def user_match_password_use_case_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=UserVerifyPasswordUseCase)  # type: ignore


@pytest.fixture()
def authorization_port_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=AuthorizationPortProtocol)  # type: ignore


@pytest.fixture()
def auth_facade(
    authorization_port_mock: Mock,
    user_get_query_mock: Mock,
    user_match_password_use_case_mock: Mock,
) -> AuthFacade:
    return AuthFacade(
        config=AuthConfig(
            access_token_ttl=10,
            refresh_token_ttl=10,
        ),
        authorization=authorization_port_mock,
        user_get_query=user_get_query_mock,
        user_match_password_use_case=user_match_password_use_case_mock,
    )
