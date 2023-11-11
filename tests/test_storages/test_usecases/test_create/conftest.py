import uuid

import pytest
from pytest_mock import MockerFixture

from src.storages.usecases import (
    StorageCreateInput,
    StorageCreateRepoInterface,
    StorageCreateUseCase,
)


@pytest.fixture()
def usecase(mocker: MockerFixture) -> StorageCreateUseCase:
    return StorageCreateUseCase(
        storage_repo=mocker.Mock(spec=StorageCreateRepoInterface),
    )


@pytest.fixture()
def input_() -> StorageCreateInput:
    link_to_storage = "https://www.fake_storage.com/123456789"
    return StorageCreateInput(
        link=link_to_storage,
        expenses_table_link=f"{link_to_storage}/expenses",
        income_table_link=f"{link_to_storage}/income",
        user_id=uuid.uuid4(),
    )
