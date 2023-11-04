import abc
import uuid
from typing import TypedDict

from src.storages.entities import Storage


class Filter(TypedDict, total=False):
    id: uuid.UUID
    user_id: uuid.UUID
    link: str
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
