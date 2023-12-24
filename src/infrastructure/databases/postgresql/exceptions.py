class PostgreSQLIsNotConnectedError(Exception):
    def __init__(self) -> None:
        super().__init__("PostgreSQL is not connected, use `connect` context manager to connect to database")
