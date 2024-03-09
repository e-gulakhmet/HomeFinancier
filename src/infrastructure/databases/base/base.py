import abc
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator, Generic, TypeVar

from .exceptions import (
    DatabaseConnectionIsAlreadyInitializedError,
    DatabaseConnectionIsNotInitializedError,
    DatabaseIsAlreadyConnectedError,
    DatabaseIsNotConnectedError,
)

Connection = TypeVar("Connection")


class DatabaseEngineInterface(abc.ABC, Generic[Connection]):
    @abc.abstractmethod
    async def connect(self) -> None: ...

    @abc.abstractmethod
    async def disconnect(self) -> None: ...

    @abc.abstractmethod
    async def acquire(self) -> Connection: ...

    @abc.abstractmethod
    async def release(self, conn: Connection) -> None: ...


class Database(Generic[Connection]):
    def __init__(self, engine: DatabaseEngineInterface[Connection]) -> None:
        self._engine = engine
        self._is_connected = False
        self._ctx_var_connection: ContextVar[Connection] = ContextVar("connection")

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[None, None]:
        if self._is_connected:
            raise DatabaseIsAlreadyConnectedError
        await self._engine.connect()
        self._is_connected = True
        try:
            yield
        finally:
            await self._engine.disconnect()
            self._is_connected = False

    @property
    def connection(self) -> Connection:
        """Rerturns Connection that assigned to current context (asyncio.Task or Thread)

        Connection is saved in context variable, so it can be accessed from any place in code.
        Check https://peps.python.org/pep-0567/ for more details about context variables.
        """
        if not self._is_connected:
            raise DatabaseIsNotConnectedError
        session = self._ctx_var_connection.get(None)
        if session is None:
            raise DatabaseConnectionIsNotInitializedError
        return session

    @asynccontextmanager
    async def open_curr_context_connection(self) -> AsyncGenerator[Connection, None]:
        if not self._is_connected:
            raise DatabaseIsNotConnectedError
        session = self._ctx_var_connection.get(None)
        if session is not None:
            raise DatabaseConnectionIsAlreadyInitializedError

        session = await self._engine.acquire()

        ctx_var_token = self._ctx_var_connection.set(session)
        try:
            yield session
        finally:
            self._ctx_var_connection.reset(ctx_var_token)
            await self._engine.release(session)
