from typing import Any

from src.foundation.email import Email
from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import HashedPassword, User, UserGetQueryProtocol, UserID


class PostgreSQLUserGetQuery(UserGetQueryProtocol):
    def __init__(self, db: Database[PostgreSQLConnection]) -> None:
        self._db = db

    async def query(self, filter_: UserGetQueryProtocol.Filter) -> User | None:
        conditions: list[str] = []
        parameters: list[Any] = []
        if "user_id" in filter_:
            conditions.append(f"id = ${len(conditions) + 1}")
            parameters.append(filter_["user_id"])
        if "email" in filter_:
            conditions.append(f"email = ${len(conditions) + 1}")
            parameters.append(filter_["email"])

        if not conditions:
            return None

        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM users WHERE {where_clause} LIMIT 1"  # noqa: S608
        record = await self._db.connection.fetchrow(query, *parameters)

        if not record:
            return None

        return User(
            id=UserID(record["id"]),
            created_at=record["created_at"],
            updated_at=record["updated_at"],
            email=Email(record["email"]),
            password=HashedPassword(record["password_hash"].encode()),
        )
