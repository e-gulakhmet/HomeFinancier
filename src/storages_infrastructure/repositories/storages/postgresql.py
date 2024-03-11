from gspread import Client as GoogleSheetsClient
from gspread import SpreadsheetNotFound

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages import OwnerID, Storage, StorageLink


class PostgreSQLGoogleSheetsStoragesRepository:
    def __init__(self, db: Database[PostgreSQLConnection], gsc: GoogleSheetsClient) -> None:
        self._db = db
        self._gsc = gsc

    async def save(self, storage: Storage) -> None:
        stmt = """
            INSERT INTO storages (id, created_at, owner_id, link, expenses_table_link, income_table_link)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self._db.connection.execute(
            stmt,
            storage.id,
            storage.created_at,
            storage.owner_id,
            storage.link,
            storage.expenses_table_link,
            storage.income_table_link,
        )

    async def exists(self, owner_id: OwnerID) -> bool:
        stmt = "SELECT 1 FROM storages WHERE owner_id = $1"
        result = await self._db.connection.fetchval(stmt, owner_id)
        return bool(result)

    async def is_accessable(self, link: StorageLink) -> bool:
        try:
            self._gsc.open_by_url(link)
        except SpreadsheetNotFound:
            return False
        return True
