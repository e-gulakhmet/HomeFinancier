from dataclasses import dataclass
from datetime import datetime

from src.transactions.types import Amount, Category, OwnerID, StorageLink


@dataclass
class Transaction:
    owner_id: OwnerID
    storage_link: StorageLink
    amount: Amount
    category: Category
    subcategory: str
    created_at: datetime
