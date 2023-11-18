import abc
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.expenses.entities import Expense
from src.expenses.exceptions import UserShouldHavePrimaryStorageError
from src.storages.entities import Storage
from src.storages.usecases import StorageGetUseCase


class ExpenseCreateRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def save(self, expense: Expense) -> None:
        ...


@dataclass
class ExpenseCreateInput:
    user_id: uuid.UUID
    amount: float
    category: str
    subcategory: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class ExpenseCreateUseCase:
    def __init__(
        self,
        expense_repo: ExpenseCreateRepoInterface,
        storage_get_usecase: StorageGetUseCase,
    ) -> None:
        self._expense_repo = expense_repo
        self._storage_get_usecase = storage_get_usecase

    async def execute(self, input_: ExpenseCreateInput) -> Expense:
        # Getting User's Primary Storage
        storage = await self._storage_get_usecase.execute(filter_={"user_id": input_.user_id, "primary": True})
        if not storage:
            raise UserShouldHavePrimaryStorageError

        # Creating domain entity
        expense = self._create_domain(input_=input_, storage=storage)

        # Saving Storage to repository
        await self._expense_repo.save(expense=expense)

        return expense

    def _create_domain(self, input_: ExpenseCreateInput, storage: Storage) -> Expense:
        return Expense(
            user_id=input_.user_id,
            exepenses_storage_link=storage.expenses_table_link,
            amount=input_.amount,
            category=input_.category,
            subcategory=input_.subcategory,
            created_at=input_.created_at,
        )
