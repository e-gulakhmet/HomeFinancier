from dataclasses import dataclass, field
from datetime import datetime

from src.storages import OwnerID as StorageOwnerID
from src.storages import StorageGetQueryProtocol
from src.transactions.entities import Transaction
from src.transactions.exceptions import UserShouldHavePrimaryStorageError
from src.transactions.repositories import TransactionsRepositoryProtocol
from src.transactions.types import Amount, Category, OwnerID, StorageLink, TransactionType


@dataclass(frozen=True)
class TransactionCreateInput:
    owner_id: OwnerID
    type_: TransactionType
    amount: Amount
    category: Category
    subcategory: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class TransactionCreateUseCase:
    def __init__(
        self,
        transactions_repo: TransactionsRepositoryProtocol,
        storage_get_query: StorageGetQueryProtocol,
    ) -> None:
        self._transaction_repo = transactions_repo
        self._storage_get_query = storage_get_query

    async def execute(self, input_: TransactionCreateInput) -> Transaction:
        # Getting User's Primary Storage
        storage = await self._storage_get_query.query(
            filter_={"owner_id": StorageOwnerID(input_.owner_id), "primary": True},
        )
        if not storage:
            raise UserShouldHavePrimaryStorageError

        transaction = Transaction(
            owner_id=input_.owner_id,
            type_=input_.type_,
            storage_link=StorageLink(storage.expenses_table_link),
            amount=input_.amount,
            category=input_.category,
            subcategory=input_.subcategory,
            created_at=input_.created_at,
        )

        await self._transaction_repo.save(transaction)

        return transaction
