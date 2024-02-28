import uuid

import pytest

from src.expenses import Amount, Category, Expense, ExpensesStorageLink
from src.expenses import OwnerID as ExpenseOwnerID
from src.storages import OwnerID as StorageOwnerID
from src.storages import Storage, StorageLink
from src.users import Email, HashedPassword, User


@pytest.fixture()
def user() -> User:
    return User(
        email=Email("example@email.com"),
        password=HashedPassword(b"some_password"),
    )


@pytest.fixture()
def storage() -> Storage:
    return Storage(
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
