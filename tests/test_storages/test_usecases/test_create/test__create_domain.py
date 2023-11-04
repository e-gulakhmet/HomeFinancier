# pyright: reportPrivateUsage=false

from src.storages.entities import Storage
from src.storages.usecases import StorageCreateInput, StorageCreateUseCase


async def test_domain_entity_is_created(usecase: StorageCreateUseCase, input_: StorageCreateInput) -> None:
    storage = usecase._create_domain(input_)

    assert isinstance(storage, Storage)
    assert storage.id is not None
    assert storage.created_at is not None
    assert storage.link == input_.link
    assert storage.user_id == input_.user_id
    assert storage.primary is False
