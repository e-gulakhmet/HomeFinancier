from dataclasses import dataclass
from datetime import datetime

from src.storages.types import OwnerID, StorageID, StorageLink


@dataclass
class Storage:
    id: StorageID
    created_at: datetime
    link: StorageLink
    expenses_table_link: StorageLink
    income_table_link: StorageLink
    owner_id: OwnerID
    primary: bool = False
