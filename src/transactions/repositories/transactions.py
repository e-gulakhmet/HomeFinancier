from typing import Protocol

from src.transactions.entities import Transaction
from src.transactions.types import StorageLink


class TransactionsNoStorageByLinkError(Exception):
    def __init__(self, link: StorageLink) -> None:
        super().__init__(f"No Storage by link: {link}")


class TransactionsRepositoryProtocol(Protocol):
    async def save(self, transaction: Transaction) -> None: ...
