from typing import Protocol

from src.storages.entities import Storage
from src.storages.types import OwnerID, StorageLink


class StoragesRepositoryProtocol(Protocol):
    async def save(self, storage: Storage) -> None:
        ...

    async def exists(self, owner_id: OwnerID) -> bool:
        ...

    async def is_accessable(self, link: StorageLink) -> bool:
        ...
