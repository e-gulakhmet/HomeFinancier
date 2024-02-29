from typing import Protocol


class IsExistsUserQueryProtocol(Protocol):
    async def query(self, user_id: int) -> bool:
        ...
