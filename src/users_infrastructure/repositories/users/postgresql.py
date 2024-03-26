from typing import Any

from src.foundation.email import Email
from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import HashedPassword, User, UserID, UsersRepositoryGetFilter


class PostgreSQLUsersRepository:
    def __init__(self, db: Database[PostgreSQLConnection]) -> None:
        self._db = db

    async def save(self, user: User) -> None:
        stmt = """
            INSERT INTO users (id, created_at, updated_at, email, password_hash)
            VALUES ($1, $2, $3, $4, $5)
        """
        await self._db.connection.execute(
            stmt,
            user.id,
            user.created_at,
            user.updated_at,
            user.email,
            user.password.decode(),
        )

    async def exists(self, email: str) -> bool:
        stmt = "SELECT 1 FROM users WHERE email = $1"
        result = await self._db.connection.fetchval(
            stmt,
            email,
        )
        return bool(result)

    async def get(self, filter_: UsersRepositoryGetFilter) -> User | None:
        conditions: list[str] = []
        params: list[Any] = []
        if "user_id" in filter_:
            conditions.append(f"id = ${len(params) + 1}")
            params.append(filter_["user_id"])

        where_clause = " AND ".join(conditions)
        stmt = f"SELECT * FROM users WHERE {where_clause} LIMIT 1"  # noqa: S608
        record = await self._db.connection.fetchrow(
            stmt,
            *params,
        )

        if not record:
            return None
        return User(
            id=UserID(record["id"]),
            created_at=record["created_at"],
            updated_at=record["updated_at"],
            email=Email(record["email"]),
            password=HashedPassword(record["password_hash"].encode()),
        )
