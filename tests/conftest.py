import uuid

import pytest

from src.storages.entities import Storage
from src.users.entities import User


@pytest.fixture()
def user() -> User:
    return User(
        email="example@email.com",
        password=b"some_password",
    )


@pytest.fixture()
def storage() -> Storage:
    return Storage(
        link="https://www.example.com",
        expenses_table_link="https://www.example.com/expenses",
        income_table_link="https://www.example.com/income",
        user_id=uuid.uuid4(),
    )
