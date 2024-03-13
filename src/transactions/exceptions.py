from src.transactions.types import StorageLink


class UserShouldHavePrimaryStorageError(Exception):
    def __init__(self) -> None:
        super().__init__("User should have primary Storage")


class StorageLinkIsUnavailableError(Exception):
    def __init__(self, storage_link: StorageLink) -> None:
        super().__init__(f"Storage is unavailable: {storage_link}")
