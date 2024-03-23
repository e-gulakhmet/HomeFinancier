from unittest.mock import Mock

import pytest

from src.auth import AuthFacade, RefreshedAuthorizationCredentials, RefreshToken, Token
from src.auth.types import AccessToken
from src.users import User


@pytest.fixture()
def refresh_token() -> RefreshToken:
    return RefreshToken(Token("refresh_token"))


@pytest.fixture()
def refreshed_authorization_credentials() -> RefreshedAuthorizationCredentials:
    return RefreshedAuthorizationCredentials(
        access_token=AccessToken(Token("new_access_token")),
        refresh_token=RefreshToken(Token("new_refresh_token")),
    )


async def test_new_authorization_credentials_are_returned(
    auth_facade: AuthFacade,
    refresh_token: RefreshToken,
    refreshed_authorization_credentials: RefreshedAuthorizationCredentials,
    authorization_port_mock: Mock,
    user: User,
) -> None:
    authorization_port_mock.get_user_id.return_value = user.id
    authorization_port_mock.gen_auth_credentials.return_value = refreshed_authorization_credentials

    result = await auth_facade.refresh_credentials(refresh_token)

    assert result == refreshed_authorization_credentials
