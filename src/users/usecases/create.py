import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from src.exceptions.core import ValidationError
from src.foundation.email import Email
from src.foundation.password import Password
from src.users.entities import User
from src.users.ports import HashingPortProtocol
from src.users.repositories import UsersRepositoryProtocol
from src.users.types import UserID


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
            id=UserID(uuid.uuid4()),
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
            email=input_.email,
            password=hashed_password,
        )

        await self._user_repo.save(user)

        return user
