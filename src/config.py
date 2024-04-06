from os import getenv


class Config:
    def __init__(self) -> None:
        self.postgresql_dsn = getenv("POSTGRESQL_DSN", "")
        self.grpc_host = getenv("GRPC_HOST", "")
        self.grpc_port = int(getenv("GRPC_PORT", ""))
