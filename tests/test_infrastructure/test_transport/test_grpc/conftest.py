from typing import AsyncGenerator
from unittest.mock import Mock

import grpc
import pytest
from pytest_mock import MockerFixture

from src.infrastructure.transport.grpc import gRPCServer, gRPCUsersService
from src.users import UserCreateUseCase


@pytest.fixture(scope="module")
def user_create_use_case_mock(module_mocker: MockerFixture) -> Mock:
    return module_mocker.Mock(spec=UserCreateUseCase)  # type: ignore


@pytest.fixture(scope="module")
def users_service(user_create_use_case_mock: Mock) -> gRPCUsersService:
    return gRPCUsersService(user_create_use_case=user_create_use_case_mock)


@pytest.fixture(scope="module", autouse=True)
async def grpc_server(users_service: gRPCUsersService) -> gRPCServer:
    server = gRPCServer(users_service=users_service)
    await server.start(host="localhost", port=50051)
    return server


@pytest.fixture(scope="module")
async def grpc_client() -> AsyncGenerator[grpc.aio.Channel, None]:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        yield channel
