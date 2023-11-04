import abc
import re
import uuid
from dataclasses import dataclass

from src.exceptions import ValidationError
from src.storages.entities import Storage
from src.users.usecases import UserExistUseCase


class StorageCreateRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def save(self, storage: Storage) -> None:
        ...

    @abc.abstractmethod
    async def exists(self, user_id: uuid.UUID, primary: bool) -> bool:
        ...

    @abc.abstractmethod
    async def is_accessable(self, link: str) -> bool:
        ...


@dataclass
class StorageCreateInput:
    link: str
    user_id: uuid.UUID


class StorageCreateUseCase:
    def __init__(
            self,
            storage_repo: StorageCreateRepoInterface,
            user_exist_usecase: UserExistUseCase,
    ) -> None:
        self._storage_repo = storage_repo
        self._user_exist_usecase = user_exist_usecase

    async def execute(self, input_: StorageCreateInput) -> Storage:
        # Validating input
        await self._validate(input_=input_)

        # Creating domain entity
        storage = self._create_domain(input_=input_)

        # Setting primary flag to Storage
        # If User has no primary storage, then set primary flag to True
        storage.primary = bool(not await self._storage_repo.exists(user_id=input_.user_id, primary=True))

        # Saving Storage to repository
        await self._storage_repo.save(storage=storage)

        return storage

    async def _validate(self, input_: StorageCreateInput) -> None:
        await self._validate_storage_link(link=input_.link)

        if not await self._user_exist_usecase.execute(user_id=input_.user_id):
            raise ValidationError(field="user_id", message="User does not exist")

    async def _validate_storage_link(self, link: str) -> None:
        if not self._is_correct_storage_link_format(link=link):
            raise ValidationError(field="link", message="Invalid link to Storage")

        if not await self._storage_repo.is_accessable(link=link):
            raise ValidationError(field="link", message="Storage is not accessable")

    def _is_correct_storage_link_format(self, link: str) -> bool:
        # Check if link is Google Sheets link
        pattern = r"https:\/\/docs\.google\.com\/spreadsheets\/d\/[a-zA-Z0-9_-]+"
        return re.match(pattern=pattern, string=link) is not None

    def _create_domain(self, input_: StorageCreateInput) -> Storage:
        return Storage(
            link=input_.link,
            user_id=input_.user_id,
        )
