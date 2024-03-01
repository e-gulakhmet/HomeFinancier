from typing import Protocol

from src.users.entities.user import User


class UsersRepositoryProtocol(Protocol):
    async def save(self, user: User) -> None:
        ...

    async def exists(self, email: str) -> bool:
        ...
