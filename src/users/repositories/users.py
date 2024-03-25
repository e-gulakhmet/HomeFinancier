from typing import Protocol, TypedDict

from src.users.entities.user import User
from src.users.types import UserID


class UsersRepositoryGetFilter(TypedDict, total=False):
    user_id: UserID


class UsersRepositoryProtocol(Protocol):
    async def save(self, user: User) -> None: ...

    async def exists(self, email: str) -> bool: ...

    async def get(self, filter_: UsersRepositoryGetFilter) -> User | None: ...
