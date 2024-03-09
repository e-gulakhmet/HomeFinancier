class DatabaseIsAlreadyConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database is already connected")


class DatabaseIsNotConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database is not connected, use `connect` context manager to connect to database")


class DatabaseConnectionIsAlreadyInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database connection is already initialized")


class DatabaseConnectionIsNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Database connection is not initialized, use `pool_context` context manager to initialize connection",
        )
