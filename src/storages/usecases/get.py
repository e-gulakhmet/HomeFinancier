import abc
from typing import TypedDict

from src.storages.entities import Storage
from src.storages.types import OwnerID, StorageID, StorageLink


class Filter(TypedDict, total=False):
    id: StorageID
    owner_id: OwnerID
    link: StorageLink
    primary: bool


class StorageGetRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def get(self, filter_: Filter) -> Storage:
        ...


class StorageGetUseCase:
    def __init__(self, storage_repo: StorageGetRepoInterface) -> None:
        self._storage_repo = storage_repo

    async def execute(self, filter_: Filter) -> Storage:
        return await self._storage_repo.get(filter_=filter_)
