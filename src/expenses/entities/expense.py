from dataclasses import dataclass
from datetime import datetime

from src.expenses.types import Amount, Category, ExpensesStorageLink, OwnerID


@dataclass
class Expense:
    owner_id: OwnerID
    expenses_storage_link: ExpensesStorageLink
    amount: Amount
    category: Category
    subcategory: str
    created_at: datetime
