from unittest.mock import Mock

import pytest

from src.auth import AccessToken, AuthFacade, Token
from src.users import User


@pytest.fixture()
def access_token() -> AccessToken:
    return AccessToken(Token("access_token"))


async def test_user_id_is_returned(
    auth_facade: AuthFacade,
    authorization_port_mock: Mock,
    access_token: AccessToken,
    user: User,
) -> None:
    authorization_port_mock.get_user_id.return_value = user.id

    result = await auth_facade.get_user_id(access_token)

    assert result == user.id
