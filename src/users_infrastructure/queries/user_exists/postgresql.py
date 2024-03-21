from uuid import UUID

from src.infrastructure.databases import Database, PostgreSQLConnection


class PostgreSQLUserExistsQuery:
    def __init__(self, db: Database[PostgreSQLConnection]) -> None:
        self._db = db

    async def query(self, user_id: UUID) -> bool:
        stmt = "SELECT 1 FROM users WHERE id = $1"
        result = await self._db.connection.fetchval(stmt, user_id)
        return bool(result)
