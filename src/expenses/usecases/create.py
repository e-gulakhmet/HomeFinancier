from dataclasses import dataclass, field
from datetime import datetime

from src.expenses.entities import Expense
from src.expenses.exceptions import UserShouldHavePrimaryStorageError
from src.expenses.repositories import ExpensesRepositoryProtocol
from src.expenses.types import Amount, Category, ExpensesStorageLink, OwnerID
from src.storages import OwnerID as StorageOwnerID
from src.storages import StorageGetQueryProtocol


@dataclass
class ExpenseCreateInput:
    owner_id: OwnerID
    amount: Amount
    category: Category
    subcategory: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class ExpenseCreateUseCase:
    def __init__(
        self,
        expense_repo: ExpensesRepositoryProtocol,
        storage_get_query: StorageGetQueryProtocol,
    ) -> None:
        self._expense_repo = expense_repo
        self._storage_get_query = storage_get_query

    async def execute(self, input_: ExpenseCreateInput) -> Expense:
        # Getting User's Primary Storage
        storage = await self._storage_get_query.query(
            filter_={"owner_id": StorageOwnerID(input_.owner_id), "primary": True},
        )
        if not storage:
            raise UserShouldHavePrimaryStorageError

        expense = Expense(
            owner_id=input_.owner_id,
            expenses_storage_link=ExpensesStorageLink(storage.expenses_table_link),
            amount=input_.amount,
            category=input_.category,
            subcategory=input_.subcategory,
            created_at=input_.created_at,
        )

        await self._expense_repo.save(expense)

        return expense
