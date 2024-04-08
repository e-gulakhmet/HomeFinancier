import logging

import homefinancier.users.v1.users_pb2 as users_pb2  # noqa: PLR0402
import homefinancier.users.v1.users_pb2_grpc as users_pb2_grpc  # noqa: PLR0402
from grpc_reflection.v1alpha import reflection

import grpc


class gRPCServer:  # noqa: N801 # gRPCServer looks better than GPRCServer (https://docs.astral.sh/ruff/rules/invalid-class-name/)
    def __init__(self, users_service: users_pb2_grpc.UsersServiceServicer) -> None:
        self._users_service = users_service
        self._server = grpc.aio.server()
        users_pb2_grpc.add_UsersServiceServicer_to_server(self._users_service, self._server)

    def enable_reflection(self) -> None:
        sevice_names = (
            users_pb2.DESCRIPTOR.services_by_name["UsersService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(sevice_names, self._server)

    async def start(self, host: str, port: int) -> None:
        address = f"{host}:{port}"
        self._server.add_insecure_port(address)

        logging.info("Starting gRPC server on %s", address)
        await self._server.start()

    async def wait_for_termination(self) -> None:
        await self._server.wait_for_termination()
