from typing import Protocol

from src.users.types import HashedPassword, Password


class HashingPortProtocol(Protocol):
    async def hash_password(self, password: Password) -> HashedPassword:
        ...
