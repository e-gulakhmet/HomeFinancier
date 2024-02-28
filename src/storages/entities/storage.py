import datetime
import uuid
from dataclasses import dataclass, field

from src.storages.types import OwnerID, StorageID, StorageLink


@dataclass
class Storage:
    link: StorageLink
    expenses_table_link: StorageLink
    income_table_link: StorageLink
    owner_id: OwnerID
    primary: bool = False

    id: StorageID = field(default_factory=lambda: StorageID(uuid.uuid4()))
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
