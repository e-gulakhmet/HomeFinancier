import uuid
from datetime import datetime, timezone

import pytest

from src.expenses import Amount, Category, Expense, ExpensesStorageLink
from src.expenses import OwnerID as ExpenseOwnerID
from src.storages import OwnerID as StorageOwnerID
from src.storages import Storage, StorageID, StorageLink
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
def expense() -> Expense:
    return Expense(
        owner_id=ExpenseOwnerID(uuid.uuid4()),
        expenses_storage_link=ExpensesStorageLink("https://www.example.com/expenses"),
        amount=Amount(100),
        category=Category("Rent"),
        subcategory="Cleaning",
    )
