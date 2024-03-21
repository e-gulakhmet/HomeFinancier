from typing import Protocol, TypedDict

from src.storages.entities import Storage
from src.storages.types import OwnerID, StorageID


class StorageGetQueryProtocol(Protocol):
    class Filter(TypedDict, total=False):
        id: StorageID
        owner_id: OwnerID
        primary: bool

    async def query(self, filter_: Filter) -> Storage | None: ...
