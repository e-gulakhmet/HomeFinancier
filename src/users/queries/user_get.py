from typing import Protocol, TypedDict

from src.foundation.email import Email
from src.users.entities.user import User
from src.users.types import UserID


class UserGetQueryProtocol(Protocol):
    class Filter(TypedDict, total=False):
        user_id: UserID
        email: Email

    async def query(self, filter_: "UserGetQueryProtocol.Filter") -> User | None: ...
