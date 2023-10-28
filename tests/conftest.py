import pytest

from src.users.entities import User


@pytest.fixture()
def user() -> User:
    return User(
        email="example@email.com",
        password=b"some_password",
    )
