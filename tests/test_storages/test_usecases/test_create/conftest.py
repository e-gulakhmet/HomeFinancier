import uuid

import pytest
from pytest_mock import MockerFixture

from src.storages import (
    OwnerID,
    StorageCreateInput,
    StorageCreateRepoInterface,
    StorageCreateUseCase,
    StorageLink,
)


@pytest.fixture()
def usecase(mocker: MockerFixture) -> StorageCreateUseCase:
    return StorageCreateUseCase(
        storage_repo=mocker.Mock(spec=StorageCreateRepoInterface),
    )


@pytest.fixture()
def input_() -> StorageCreateInput:
    link_to_storage = StorageLink("https://docs.google.com/spreadsheets/d/torirejfklsjdf324234klj4234")
    expenses_table_link = StorageLink(f"{link_to_storage}/expenses")
    income_table_link = StorageLink(f"{link_to_storage}/income")
    return StorageCreateInput(
        link=link_to_storage,
        expenses_table_link=expenses_table_link,
        income_table_link=income_table_link,
        owner_id=OwnerID(uuid.uuid4()),
    )
