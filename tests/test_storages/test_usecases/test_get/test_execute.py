# pyright: reportPrivateUsage=false

import uuid

from pytest_mock import MockerFixture

from src.storages.entities import Storage
from src.storages.usecases import StorageGetUseCase


async def test__storage_repo_is_called_to_get_storage(usecase: StorageGetUseCase, mocker: MockerFixture) -> None:
    user_id = uuid.uuid4()
    storage_id = uuid.uuid4()
    primary = True
    spy = mocker.spy(usecase._storage_repo, "get")

    await usecase.execute(filter_={"user_id": user_id, "id": storage_id, "primary": primary})

    spy.assert_called_once_with(user_id=user_id, id=storage_id, primary=primary)


async def test__storage_repo_response_is_returned(
        usecase: StorageGetUseCase, mocker: MockerFixture, storage: Storage) -> None:
    mocker.patch.object(usecase._storage_repo, "get", return_value=storage)

    result = await usecase.execute(filter_={"primary": True})

    assert result == storage
