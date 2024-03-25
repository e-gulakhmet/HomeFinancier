from dataclasses import dataclass
from typing import Protocol

from src.auth.types import AccessToken, RefreshToken, Token
from src.users import UserID


class TokenIsInvalidError(Exception):
    """Raised when token is invalid."""


class TokenIsExpiredError(Exception):
    """Raised when token is expired."""


@dataclass(frozen=True)
class GenAuthCredentialsInput:
    user_id: UserID
    access_ttl: int
    refresh_ttl: int


@dataclass(frozen=True)
class GenAuthCredentialsOutput:
    access_token: AccessToken
    refresh_token: RefreshToken


class AuthorizationPortProtocol(Protocol):
    async def gen_auth_credentials(self, input_: GenAuthCredentialsInput) -> GenAuthCredentialsOutput:
        """Generates Authorization credentials with User's information."""
        ...

    async def get_user_id(self, access_token: Token) -> UserID:
        """Parses token and returns User's ID."""
        ...
