from unittest.mock import Mock

import pytest

from src.auth import (
    AccessToken,
    AuthenticationCredentials,
    AuthFacade,
    AuthorizationCredentials,
    InvalidEmailOrPasswordError,
    RefreshToken,
    Token,
)
from src.foundation.email import Email
from src.foundation.password import Password
from src.users import User


@pytest.fixture()
def login_input() -> AuthenticationCredentials:
    return AuthenticationCredentials(
        email=Email("example@example.com"),
        password=Password("example_password"),
    )


@pytest.fixture()
def auth_credentials() -> AuthorizationCredentials:
    return AuthorizationCredentials(
        access_token=AccessToken(Token("access_token")),
        refresh_token=RefreshToken(Token("refresh_token")),
    )


async def test_access_and_refresh_tokens_are_returned_if_user_email_and_password_are_correct(  # noqa: PLR0913
    auth_facade: AuthFacade,
    user_get_query_mock: Mock,
    user_match_password_use_case_mock: Mock,
    authorization_port_mock: Mock,
    login_input: AuthenticationCredentials,
    user: User,
    auth_credentials: AuthorizationCredentials,
) -> None:
    user_get_query_mock.query.return_value = user
    user_match_password_use_case_mock.execute.return_value = True
    authorization_port_mock.gen_auth_credentials.return_value = auth_credentials

    auth_credentials = await auth_facade.login(login_input)

    assert auth_credentials.access_token
    assert auth_credentials.refresh_token


async def test_error_if_user_with_specified_email_does_not_exist(
    auth_facade: AuthFacade,
    user_get_query_mock: Mock,
    login_input: AuthenticationCredentials,
) -> None:
    user_get_query_mock.query.return_value = None

    with pytest.raises(InvalidEmailOrPasswordError):
        await auth_facade.login(login_input)


async def test_error_if_password_is_incorrect(
    auth_facade: AuthFacade,
    user_get_query_mock: Mock,
    user_match_password_use_case_mock: Mock,
    login_input: AuthenticationCredentials,
    user: User,
) -> None:
    user_get_query_mock.query.return_value = user
    user_match_password_use_case_mock.execute.return_value = False

    with pytest.raises(InvalidEmailOrPasswordError):
        await auth_facade.login(login_input)
