from src.infrastructure.databases import Database, PostgreSQLConnection
from src.users import User


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
            str(user.password),
        )

    async def exists(self, email: str) -> bool:
        stmt = "SELECT 1 FROM users WHERE email = $1"
        result = await self._db.connection.fetchval(
            stmt,
            email,
        )
        return bool(result)
