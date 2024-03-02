import uuid
from datetime import datetime, timezone

import pytest

from src.storages import OwnerID as StorageOwnerID
from src.storages import Storage, StorageID, StorageLink
from src.transactions import Amount, Category, Transaction, TransactionType
from src.transactions import OwnerID as TransactionOwnerID
from src.transactions import StorageLink as TransactionsStorageLink
from src.users import Email, HashedPassword, User, UserID


@pytest.fixture()
def user() -> User:
    return User(
        id=UserID(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        updated_at=datetime.now(tz=timezone.utc),
        email=Email("example@email.com"),
        password=HashedPassword(b"some_password"),
    )


@pytest.fixture()
def storage() -> Storage:
    return Storage(
        id=StorageID(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        expenses_table_link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        income_table_link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        owner_id=StorageOwnerID(uuid.uuid4()),
    )


@pytest.fixture()
def transaction() -> Transaction:
    return Transaction(
        created_at=datetime.now(tz=timezone.utc),
        owner_id=TransactionOwnerID(uuid.uuid4()),
        storage_link=TransactionsStorageLink("https://www.example.com/expenses"),
        type_=TransactionType.EXPENSE,
        amount=Amount(100),
        category=Category("Rent"),
        subcategory="Cleaning",
    )
