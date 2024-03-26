import uuid
from datetime import datetime, timedelta, timezone

import pytest

from src.auth.ports.authorization import GenAuthCredentialsInput
from src.auth_infrastructure.adapters.authorization.jwt import JWTAuthorization
from src.users import UserID
from tests.test_auth_infrasturcture.test_adapters.test_authorization.test_jwt.utils import decode_token


@pytest.fixture()
def gen_auth_credentials_input() -> GenAuthCredentialsInput:
    return GenAuthCredentialsInput(
        user_id=UserID(uuid.uuid4()),
        access_ttl=3600,
        refresh_ttl=7200,
    )


async def test_auth_credentials_is_issued_successfully(
    jwt_authorization: JWTAuthorization,
    gen_auth_credentials_input: GenAuthCredentialsInput,
) -> None:
    credentials = await jwt_authorization.gen_auth_credentials(gen_auth_credentials_input)

    assert credentials.access_token is not None
    assert credentials.refresh_token is not None


class TestAccessToken:
    async def test_access_token_payload_contains_user_id(
        self,
        jwt_authorization: JWTAuthorization,
        gen_auth_credentials_input: GenAuthCredentialsInput,
        secret_key: str,
        algorithm: str,
    ) -> None:
        credentials = await jwt_authorization.gen_auth_credentials(gen_auth_credentials_input)

        token_payload = decode_token(credentials.access_token, secret_key, algorithm)
        assert token_payload["user_id"] == str(gen_auth_credentials_input.user_id)

    async def test_access_token_payload_contains_exp(
        self,
        jwt_authorization: JWTAuthorization,
        gen_auth_credentials_input: GenAuthCredentialsInput,
        secret_key: str,
        algorithm: str,
    ) -> None:
        now = datetime.now(tz=timezone.utc)

        credentials = await jwt_authorization.gen_auth_credentials(gen_auth_credentials_input)

        token_payload = decode_token(credentials.access_token, secret_key, algorithm)
        assert (
            now
            <= datetime.fromtimestamp(token_payload["exp"], tz=timezone.utc)
            <= datetime.now(tz=timezone.utc) + timedelta(gen_auth_credentials_input.access_ttl)
        )


class TestRefreshToken:
    async def test_refresh_token_payload_contains_user_id(
        self,
        jwt_authorization: JWTAuthorization,
        gen_auth_credentials_input: GenAuthCredentialsInput,
        secret_key: str,
        algorithm: str,
    ) -> None:
        credentials = await jwt_authorization.gen_auth_credentials(gen_auth_credentials_input)

        token_payload = decode_token(credentials.refresh_token, secret_key, algorithm)
        assert token_payload["user_id"] == str(gen_auth_credentials_input.user_id)

    async def test_refresh_token_payload_contains_exp(
        self,
        jwt_authorization: JWTAuthorization,
        gen_auth_credentials_input: GenAuthCredentialsInput,
        secret_key: str,
        algorithm: str,
    ) -> None:
        now = datetime.now(tz=timezone.utc)

        credentials = await jwt_authorization.gen_auth_credentials(gen_auth_credentials_input)

        token_payload = decode_token(credentials.refresh_token, secret_key, algorithm)
        assert (
            now
            <= datetime.fromtimestamp(token_payload["exp"], tz=timezone.utc)
            <= datetime.now(tz=timezone.utc) + timedelta(seconds=gen_auth_credentials_input.refresh_ttl)
        )
