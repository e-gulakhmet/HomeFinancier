import uuid
from datetime import datetime, timedelta, timezone

import pytest

from src.auth import AccessToken, GenAuthCredentialsInput, Token, TokenIsExpiredError, TokenIsInvalidError
from src.auth_infrastructure.adapters.authorization.jwt import JWTAuthorization
from src.users import UserID
from tests.test_auth_infrasturcture.test_adapters.test_authorization.test_jwt.utils import encode_token


@pytest.fixture()
def user_id() -> UserID:
    return UserID(uuid.uuid4())


@pytest.fixture()
async def valid_access_token(jwt_authorization: JWTAuthorization, user_id: UserID) -> AccessToken:
    auth_credentials = await jwt_authorization.gen_auth_credentials(
        GenAuthCredentialsInput(
            user_id=user_id,
            access_ttl=10,
            refresh_ttl=10,
        ),
    )
    return auth_credentials.access_token


@pytest.fixture()
def invalid_access_token() -> AccessToken:
    return AccessToken(Token("invalid_token"))


@pytest.fixture()
def expired_access_token(secret_key: str, algorithm: str) -> AccessToken:
    token = encode_token({"exp": datetime.now(timezone.utc) - timedelta(hours=1)}, secret_key, algorithm)
    return AccessToken(token)


async def test_get_user_id_success(
    jwt_authorization: JWTAuthorization,
    valid_access_token: AccessToken,
    user_id: UserID,
) -> None:
    result = await jwt_authorization.get_user_id(valid_access_token)

    assert result == user_id


async def test_error_if_token_is_invalid(
    jwt_authorization: JWTAuthorization,
    invalid_access_token: AccessToken,
) -> None:
    with pytest.raises(TokenIsInvalidError):
        await jwt_authorization.get_user_id(invalid_access_token)


async def test_error_if_token_is_expired(
    jwt_authorization: JWTAuthorization,
    expired_access_token: AccessToken,
) -> None:
    with pytest.raises(TokenIsExpiredError):
        await jwt_authorization.get_user_id(expired_access_token)
