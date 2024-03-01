from dataclasses import dataclass

from src.exceptions import ValidationError
from src.storages.entities import Storage
from src.storages.repositories import StoragesRepositoryProtocol
from src.storages.types import OwnerID, StorageLink


@dataclass(frozen=True)
class StorageCreateInput:
    link: StorageLink
    expenses_table_link: StorageLink
    income_table_link: StorageLink
    owner_id: OwnerID


class StorageCreateUseCase:
    _STORAGE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT = "Storage link is not accessable"
    _EXPENSES_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT = "Expenses table link is not accessable"
    _INCOME_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT = "Income table link is not accessable"

    def __init__(
        self,
        storage_repo: StoragesRepositoryProtocol,
    ) -> None:
        self._storage_repo = storage_repo

    async def execute(self, input_: StorageCreateInput) -> Storage:
        await self._validate(input_=input_)

        storage = Storage(
            link=input_.link,
            expenses_table_link=input_.expenses_table_link,
            income_table_link=input_.income_table_link,
            owner_id=input_.owner_id,
        )

        if not await self._storage_repo.exists(owner_id=input_.owner_id):
            storage.primary = True

        await self._storage_repo.save(storage=storage)

        return storage

    async def _validate(self, input_: StorageCreateInput) -> None:
        if not await self._storage_repo.is_accessable(link=input_.link):
            raise ValidationError(field="link", message=self._STORAGE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT)

        if not await self._storage_repo.is_accessable(link=input_.expenses_table_link):
            raise ValidationError(
                field="expenses_table_link",
                message=self._EXPENSES_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT,
            )

        if not await self._storage_repo.is_accessable(link=input_.income_table_link):
            raise ValidationError(
                field="income_table_link",
                message=self._INCOME_TABLE_LINK_IS_NOT_ACCESSABLE_ERROR_TEXT,
            )
