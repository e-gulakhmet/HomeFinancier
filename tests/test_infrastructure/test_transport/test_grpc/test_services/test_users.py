from unittest.mock import Mock

import grpc
import pytest
from homefinancier.users.v1.users_pb2 import CreateUserRequest, CreateUserResponse
from homefinancier.users.v1.users_pb2_grpc import UsersServiceStub

from src.exceptions import ValidationError
from src.foundation.email import Email
from src.foundation.password import Password
from src.users import User


@pytest.fixture(scope="module")
def users_service_stub(grpc_client: grpc.aio.Channel) -> UsersServiceStub:
    return UsersServiceStub(grpc_client)


async def test_success(
    users_service_stub: UsersServiceStub,
    user_create_use_case_mock: Mock,
    user: User,
) -> None:
    user_create_use_case_mock.execute.return_value = user
    input_ = CreateUserRequest(
        email="example@example.com",
        password="password",
    )

    response = await users_service_stub.CreateUser(input_)

    assert isinstance(response, CreateUserResponse)
    assert response.id


async def test_error_if_email_is_incorrect(
    users_service_stub: UsersServiceStub,
) -> None:
    input_ = CreateUserRequest(
        email="example",
        password="password",
    )

    with pytest.raises(grpc.aio.AioRpcError) as exc_info:
        await users_service_stub.CreateUser(input_)

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert exc_info.value.details() == Email._INVALID_EMAIL_ERROR_TEXT


async def test_error_if_password_is_incorrect(
    users_service_stub: UsersServiceStub,
) -> None:
    input_ = CreateUserRequest(
        email="example@example.com",
        password="a",
    )

    with pytest.raises(grpc.aio.AioRpcError) as exc_info:
        await users_service_stub.CreateUser(input_)

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert exc_info.value.details() == Password._MIN_LENGTH_ERROR_TEXT


async def test_error_if_user_already_exists(
    users_service_stub: UsersServiceStub,
    user_create_use_case_mock: Mock,
) -> None:
    input_ = CreateUserRequest(
        email="example@example.com",
        password="password",
    )
    user_create_use_case_mock.execute.side_effect = ValidationError(field="email", message="already exists")

    with pytest.raises(grpc.aio.AioRpcError) as exc_info:
        await users_service_stub.CreateUser(input_)
    assert exc_info.value.code() == grpc.StatusCode.ALREADY_EXISTS
