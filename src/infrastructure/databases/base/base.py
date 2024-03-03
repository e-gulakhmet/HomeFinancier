import abc
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator, Generic, TypeVar

from .exceptions import (
    DatabaseIsAlreadyConnectedError,
    DatabaseIsNotConnectedError,
    DatabaseSessionIsAlreadyInitializedError,
    DatabaseSessionIsNotInitializedError,
)

Session = TypeVar("Session")


class DatabaseEngineInterface(abc.ABC, Generic[Session]):
    @abc.abstractmethod
    async def connect(self) -> None:
        ...

    @abc.abstractmethod
    async def disconnect(self) -> None:
        ...

    @abc.abstractmethod
    async def acquire(self) -> Session:
        ...

    @abc.abstractmethod
    async def release(self, conn: Session) -> None:
        ...


class Database(Generic[Session]):
    def __init__(self, engine: DatabaseEngineInterface[Session]) -> None:
        self._engine = engine
        self._is_connected = False
        self._ctx_var_session: ContextVar[Session] = ContextVar("session")

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
    def session(self) -> Session:
        """Rerturns Session that assigned to current context (asyncio.Task or Thread)

        Session is saved in context variable, so it can be accessed from any place in code.
        Check https://peps.python.org/pep-0567/ for more details about context variables.
        """
        if not self._is_connected:
            raise DatabaseIsNotConnectedError
        session = self._ctx_var_session.get(None)
        if session is None:
            raise DatabaseSessionIsNotInitializedError
        return session

    @asynccontextmanager
    async def session_context(self) -> AsyncGenerator[Session, None]:
        if not self._is_connected:
            raise DatabaseIsNotConnectedError
        session = self._ctx_var_session.get(None)
        if session is not None:
            raise DatabaseSessionIsAlreadyInitializedError

        session = await self._engine.acquire()

        ctx_var_token = self._ctx_var_session.set(session)
        try:
            yield session
        finally:
            self._ctx_var_session.reset(ctx_var_token)
            await self._engine.release(session)
