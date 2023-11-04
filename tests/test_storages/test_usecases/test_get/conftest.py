import pytest
from pytest_mock import MockerFixture

from src.storages.usecases import (
    StorageGetRepoInterface,
    StorageGetUseCase,
)


@pytest.fixture()
def usecase(mocker: MockerFixture) -> StorageGetUseCase:
    return StorageGetUseCase(
        storage_repo=mocker.Mock(spec=StorageGetRepoInterface),
    )
