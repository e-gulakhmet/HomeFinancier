from typing import Protocol

from src.foundation.password import Password
from src.users.types import HashedPassword


class HashingPortProtocol(Protocol):
    async def hash_password(self, password: Password) -> HashedPassword: ...
