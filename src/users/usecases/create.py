from dataclasses import dataclass

from src.exceptions.core import ValidationError
from src.users.entities import User
from src.users.ports import HashingPortProtocol
from src.users.repositories import UsersRepositoryProtocol
from src.users.types import Email, Password


@dataclass(frozen=True)
class UserCreateInput:
    email: Email
    password: Password


class UserCreateUseCase:
    def __init__(
        self,
        user_repo: UsersRepositoryProtocol,
        hashing_provider: HashingPortProtocol,
    ) -> None:
        self._user_repo = user_repo
        self._hashing_provider = hashing_provider

    async def execute(self, input_: UserCreateInput) -> User:
        if await self._user_repo.exists(email=input_.email):
            raise ValidationError(field="email", message="Email already exists")

        hashed_password = await self._hashing_provider.hash_password(input_.password)
        user = User(
            email=input_.email,
            password=hashed_password,
        )

        await self._user_repo.save(user)

        return user
