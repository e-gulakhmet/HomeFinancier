from typing import Any

from src.infrastructure.databases import Database, PostgreSQLConnection
from src.storages import Storage, StorageGetQueryProtocol, StorageLink
from src.storages.types import OwnerID, StorageID


class PostgreSQLStorageGetQuery(StorageGetQueryProtocol):
    def __init__(self, db: Database[PostgreSQLConnection]) -> None:
        self._db = db

    async def query(self, filter_: StorageGetQueryProtocol.Filter) -> Storage | None:
        conditions: list[str] = []
        parameters: list[Any] = []
        if "id" in filter_:
            conditions.append(f"id = ${len(conditions) + 1}")
            parameters.append(filter_["id"])
        if "owner_id" in filter_:
            conditions.append(f"owner_id = ${len(conditions) + 1}")
            parameters.append(filter_["owner_id"])
        # Note: 'primary' key is not present in the schema and will be ignored

        if not conditions:
            query = "SELECT * FROM storages LIMIT 1"
        else:
            where_clause = " AND ".join(conditions)
            query = f"SELECT * FROM storages WHERE {where_clause} LIMIT 1"  # noqa: S608

        record = await self._db.connection.fetchrow(query, *parameters)

        if not record:
            return None
        return Storage(
            id=StorageID(record["id"]),
            created_at=record["created_at"],
            link=StorageLink(record["link"]),
            expenses_table_link=StorageLink(record["expenses_table_link"]),
            income_table_link=StorageLink(record["income_table_link"]),
            owner_id=OwnerID(record["owner_id"]),
        )
