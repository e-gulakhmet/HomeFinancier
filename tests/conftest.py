import asyncio
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator, Generator

import pytest
from gspread import Client as GoogleSheetsClient
from pytest_mock import MockerFixture

from src.infrastructure.databases import Database, PostgreSQL, PostgreSQLConnection
from src.storages import OwnerID as StorageOwnerID
from src.storages import Storage, StorageID, StorageLink
from src.transactions import Amount, Category, Transaction, TransactionType
from src.transactions import OwnerID as TransactionOwnerID
from src.transactions import StorageLink as TransactionsStorageLink
from src.users import Email, HashedPassword, User, UserID


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgresql_engine() -> PostgreSQL:
    return PostgreSQL(dsn="postgresql://postgres:postgres@localhost:5432/homefinancier_test")


@pytest.fixture(scope="session")
async def postgresql_db(postgresql_engine: PostgreSQL) -> AsyncGenerator[Database[PostgreSQLConnection], None]:
    db = Database(engine=postgresql_engine)
    async with db.connect():
        yield db


@pytest.fixture()
def google_sheets_client_mock(mocker: MockerFixture) -> GoogleSheetsClient:
    return mocker.Mock(spec=GoogleSheetsClient)


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
def storage(user: User) -> Storage:
    return Storage(
        id=StorageID(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        expenses_table_link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        income_table_link=StorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        owner_id=StorageOwnerID(user.id),
    )


@pytest.fixture()
def transaction() -> Transaction:
    return Transaction(
        created_at=datetime.now(tz=timezone.utc),
        owner_id=TransactionOwnerID(uuid.uuid4()),
        storage_link=TransactionsStorageLink("https://docs.google.com/spreadsheets/d/1/edit"),
        type_=TransactionType.EXPENSE,
        amount=Amount(100),
        category=Category("Rent"),
    )
