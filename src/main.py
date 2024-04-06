import asyncio
import logging

from src.config import Config
from src.infrastructure.databases import Database, PostgreSQL
from src.infrastructure.transport.grpc import gRPCServer, gRPCUsersService
from src.users import UserCreateUseCase
from src.users_infrastructure import PostgreSQLUsersRepository
from src.users_infrastructure.adapters.hashing import FakeHashingAdapter


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = Config()

    posgresql = PostgreSQL(dsn=config.postgresql_dsn)
    db = Database(engine=posgresql)

    users_repository = PostgreSQLUsersRepository(db=db)
    hasging_provider = FakeHashingAdapter()
    user_create_use_case = UserCreateUseCase(user_repo=users_repository, hashing_provider=hasging_provider)

    grpc_users_service = gRPCUsersService(user_create_use_case=user_create_use_case)
    grpc_server = gRPCServer(users_service=grpc_users_service)
    grpc_server.enable_reflection()

    async with db.connect():
        await grpc_server.start(host=config.grpc_host, port=config.grpc_port)


if __name__ == "__main__":
    asyncio.run(main())
