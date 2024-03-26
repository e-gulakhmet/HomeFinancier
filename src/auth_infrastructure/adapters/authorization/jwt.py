from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from src.auth import (
    AccessToken,
    GenAuthCredentialsInput,
    GenAuthCredentialsOutput,
    RefreshToken,
    Token,
    TokenIsExpiredError,
    TokenIsInvalidError,
)
from src.users import UserID


class JWTAuthorization:
    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def gen_auth_credentials(self, input_: GenAuthCredentialsInput) -> GenAuthCredentialsOutput:
        access_token_expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=input_.access_ttl)
        refresh_token_expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=input_.refresh_ttl)

        access_payload = {
            "user_id": str(input_.user_id),
            "exp": access_token_expiration,
        }
        refresh_payload = {
            "user_id": str(input_.user_id),
            "exp": refresh_token_expiration,
        }
        access_token = jwt.encode(
            access_payload,
            self._secret_key,
            algorithm=self._algorithm,
        )
        refresh_token = jwt.encode(
            refresh_payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

        return GenAuthCredentialsOutput(
            access_token=AccessToken(Token(access_token)),
            refresh_token=RefreshToken(Token(refresh_token)),
        )

    async def get_user_id(self, access_token: Token) -> UserID:
        try:
            payload = jwt.decode(access_token, self._secret_key, algorithms=[self._algorithm])
        except jwt.ExpiredSignatureError:
            raise TokenIsExpiredError from None
        except jwt.InvalidTokenError:
            raise TokenIsInvalidError from None

        return UserID(UUID(payload["user_id"]))
