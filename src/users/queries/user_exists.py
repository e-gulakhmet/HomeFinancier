from typing import Protocol
from uuid import UUID


class UserExistsQueryProtocol(Protocol):
    async def query(self, user_id: UUID) -> bool: ...
