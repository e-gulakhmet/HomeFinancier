class DatabaseIsAlreadyConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database is already connected")


class DatabaseIsNotConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database is not connected, use `connect` context manager to connect to database")


class DatabaseSessionIsAlreadyInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("Database session is already initialized")


class DatabaseSessionIsNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Database session is not initialized, use `session_context` context manager to initialize session",
        )
