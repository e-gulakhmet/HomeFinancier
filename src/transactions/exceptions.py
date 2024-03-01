class UserShouldHavePrimaryStorageError(Exception):
    def __init__(self) -> None:
        super().__init__("User should have primary Storage")
