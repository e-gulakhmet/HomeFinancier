import abc
from dataclasses import dataclass

from src.exceptions.core import ValidationError
from src.users.entities import User
from src.users.types import Email, HashedPassword, Password


class UserCreateRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def exists(self, email: Email) -> bool:
        ...

    @abc.abstractmethod
    async def save(self, user: User) -> None:
        ...


class UserCreateHashingProviderInterface(abc.ABC):
    @abc.abstractmethod
    def hash_password(self, password: Password) -> HashedPassword:
        ...


@dataclass
class UserCreateInput:
    email: Email
    password: Password


class UserCreateUseCase:
    def __init__(
        self,
        user_repo: UserCreateRepoInterface,
        hashing_provider: UserCreateHashingProviderInterface,
    ) -> None:
        self._user_repo = user_repo
        self._hashing_provider = hashing_provider

    async def execute(self, input_: UserCreateInput) -> User:
        if await self._user_repo.exists(email=input_.email):
            raise ValidationError(field="email", message="Email already exists")

        hashed_password = self._hashing_provider.hash_password(input_.password)
        user = User(
            email=input_.email,
            password=hashed_password,
        )

        await self._user_repo.save(user)

        return user
