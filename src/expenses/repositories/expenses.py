from typing import Protocol

from src.expenses.entities import Expense


class ExpensesRepositoryProtocol(Protocol):
    async def save(self, expense: Expense) -> None:
        ...
