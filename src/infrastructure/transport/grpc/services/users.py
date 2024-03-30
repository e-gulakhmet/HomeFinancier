from homefinancier.users.v1.users_pb2 import CreateUserRequest, CreateUserResponse
from homefinancier.users.v1.users_pb2_grpc import UsersServiceServicer

import grpc
from src.exceptions.core import ValidationError
from src.foundation.email import Email
from src.foundation.password import Password
from src.users import UserCreateInput, UserCreateUseCase


class gRPCUsersService(UsersServiceServicer):  # type: ignore # noqa: N801
    def __init__(self, user_create_use_case: UserCreateUseCase) -> None:
        self.user_create_use_case = user_create_use_case

    async def CreateUser(
        self,
        request: CreateUserRequest,
        context: grpc.aio.ServicerContext[CreateUserRequest, CreateUserResponse],
    ) -> CreateUserResponse:
        try:
            user = await self.user_create_use_case.execute(
                UserCreateInput(
                    email=Email(request.email),
                    password=Password(request.password),
                ),
            )
        except ValueError as e:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
        except ValidationError as e:
            if e.field == "email":
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        response = CreateUserResponse(
            id=str(user.id),
        )
        return response
