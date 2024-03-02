from typing import Protocol

from src.transactions.entities import Transaction


class TransactionsRepositoryProtocol(Protocol):
    async def save(self, transaction: Transaction) -> None:
        ...
