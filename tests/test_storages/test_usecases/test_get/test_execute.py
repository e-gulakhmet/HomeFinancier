# pyright: reportPrivateUsage=false

import uuid

from pytest_mock import MockerFixture

from src.storages import OwnerID, Storage, StorageGetFilter, StorageGetUseCase, StorageID


async def test__storage_repo_is_called_to_get_storage(usecase: StorageGetUseCase, mocker: MockerFixture) -> None:
    user_id = uuid.uuid4()
    storage_id = uuid.uuid4()
    primary = True
    spy = mocker.spy(usecase._storage_repo, "get")
    filter_: StorageGetFilter = {"owner_id": OwnerID(user_id), "id": StorageID(storage_id), "primary": primary}

    await usecase.execute(filter_=filter_)

    spy.assert_called_once_with(filter_=filter_)


async def test__storage_repo_response_is_returned(
    usecase: StorageGetUseCase,
    mocker: MockerFixture,
    storage: Storage,
) -> None:
    mocker.patch.object(usecase._storage_repo, "get", return_value=storage)

    result = await usecase.execute(filter_={"primary": True})

    assert result == storage
