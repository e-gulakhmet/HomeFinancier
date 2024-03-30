import homefinancier.users.v1.users_pb2_grpc as users_pb2_grpc  # noqa: PLR0402

import grpc


class gRPCServer:  # noqa: N801 # gRPCServer looks better than GPRCServer (https://docs.astral.sh/ruff/rules/invalid-class-name/)
    def __init__(self, users_service: users_pb2_grpc.UsersServiceServicer) -> None:
        self._users_service = users_service
        self._server = grpc.aio.server()
        users_pb2_grpc.add_UsersServiceServicer_to_server(self._users_service, self._server)

    async def start(self, host: str, port: int) -> None:
        # Register services

        # Start server
        address = f"{host}:{port}"
        self._server.add_insecure_port(address)

        await self._server.start()
