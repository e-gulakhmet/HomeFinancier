from typing import Protocol

from src.transactions.entities import Transaction


class TransactionsRepositoryProtocol(Protocol):
    async def save(self, expense: Transaction) -> None:
        ...
