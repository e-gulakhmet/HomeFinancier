from dataclasses import dataclass

from src.foundation.password import Password
from src.users.ports.hashing import HashingPortProtocol
from src.users.repositories import UsersRepositoryProtocol
from src.users.types import UserID


@dataclass(frozen=True)
class UserVerifyPasswordInput:
    user_id: UserID
    password: Password


class UserVerifyPasswordUseCase:
    def __init__(self, user_repository: UsersRepositoryProtocol, hashing: HashingPortProtocol) -> None:
        self._user_repository = user_repository
        self._hashing = hashing

    async def execute(self, input_: UserVerifyPasswordInput) -> bool:
        user = await self._user_repository.get(filter_={"user_id": input_.user_id})
        if not user:
            return False
        return await self._hashing.verify_password(password=input_.password, hashed_password=user.password)
