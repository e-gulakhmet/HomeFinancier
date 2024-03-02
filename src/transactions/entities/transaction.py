from dataclasses import dataclass
from datetime import datetime

from src.transactions.types import Amount, Category, OwnerID, StorageLink, TransactionType


@dataclass
class Transaction:
    owner_id: OwnerID
    storage_link: StorageLink
    type_: TransactionType
    amount: Amount
    category: Category
    created_at: datetime
