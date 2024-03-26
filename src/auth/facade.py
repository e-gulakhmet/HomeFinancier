from dataclasses import dataclass

from src.auth.exceptions import InvalidEmailOrPasswordError
from src.auth.ports.authorization import AuthorizationPortProtocol, GenAuthCredentialsInput
from src.auth.types import AccessToken, RefreshToken
from src.foundation.email import Email
from src.foundation.password import Password
from src.users import UserGetQueryProtocol, UserID, UserVerifyPasswordInput, UserVerifyPasswordUseCase


@dataclass(frozen=True)
class AuthConfig:
    access_token_ttl: int
    refresh_token_ttl: int


@dataclass(frozen=True)
class AuthenticationCredentials:
    email: Email
    password: Password


@dataclass(frozen=True)
class AuthorizationCredentials:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass(frozen=True)
class RefreshedAuthorizationCredentials:
    access_token: AccessToken
    refresh_token: RefreshToken


class AuthFacade:
    """Provides operations for Access/Refresh tokens based authorization."""

    def __init__(
        self,
        config: AuthConfig,
        authorization: AuthorizationPortProtocol,
        user_get_query: UserGetQueryProtocol,
        user_match_password_use_case: UserVerifyPasswordUseCase,
    ) -> None:
        self._config = config
        self._authorization = authorization
        self._user_get_query = user_get_query
        self._user_match_password_use_case = user_match_password_use_case

    async def login(self, authentication_credentials: AuthenticationCredentials) -> AuthorizationCredentials:
        """Checks passed authentication credentials and returns authorization credentials."""

        user = await self._user_get_query.query(filter_={"email": authentication_credentials.email})
        if not user:
            raise InvalidEmailOrPasswordError

        is_password_correct = await self._user_match_password_use_case.execute(
            UserVerifyPasswordInput(
                user_id=user.id,
                password=authentication_credentials.password,
            ),
        )
        if not is_password_correct:
            raise InvalidEmailOrPasswordError

        gen_auth_credentials_output = await self._authorization.gen_auth_credentials(
            GenAuthCredentialsInput(
                user_id=user.id,
                access_ttl=self._config.access_token_ttl,
                refresh_ttl=self._config.refresh_token_ttl,
            ),
        )

        return AuthorizationCredentials(
            access_token=gen_auth_credentials_output.access_token,
            refresh_token=gen_auth_credentials_output.refresh_token,
        )

    async def get_user_id(self, access_token: AccessToken) -> UserID:
        """Returns User's ID based on Access Token."""

        user_id = await self._authorization.get_user_id(access_token)

        return user_id

    async def refresh_credentials(self, refresh_token: RefreshToken) -> RefreshedAuthorizationCredentials:
        """Checks passed  token and returns new Access Token."""

        user_id = await self._authorization.get_user_id(refresh_token)

        auth_credentials = await self._authorization.gen_auth_credentials(
            GenAuthCredentialsInput(
                user_id=user_id,
                access_ttl=self._config.access_token_ttl,
                refresh_ttl=self._config.refresh_token_ttl,
            ),
        )

        return RefreshedAuthorizationCredentials(
            access_token=auth_credentials.access_token,
            refresh_token=auth_credentials.refresh_token,
        )
