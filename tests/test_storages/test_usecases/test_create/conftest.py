import uuid

import pytest
from pytest_mock import MockerFixture

from src.storages.usecases import (
    StorageCreateInput,
    StorageCreateRepoInterface,
    StorageCreateUseCase,
)
from src.users.usecases import UserExistUseCase


@pytest.fixture()
def usecase(mocker: MockerFixture) -> StorageCreateUseCase:
    return StorageCreateUseCase(
        storage_repo=mocker.Mock(spec=StorageCreateRepoInterface),
        user_exist_usecase=mocker.Mock(spec=UserExistUseCase),
    )


@pytest.fixture()
def input_() -> StorageCreateInput:
    return StorageCreateInput(
        link="https://www.fake_storage.com/123456789",
        user_id=uuid.uuid4(),
    )
