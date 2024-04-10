from os import getenv


class Config:
    def __init__(self) -> None:
        self.postgresql_dsn = getenv("DATABASE_URL", "")
        self.test_postgresql_dsn = getenv("TEST_DATABASE_URL", "")
        self.grpc_host = getenv("GRPC_HOST", "")
        self.grpc_port = int(getenv("GRPC_PORT", ""))
