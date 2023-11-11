import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class Storage:
    link: str
    expenses_table_link: str
    income_table_link: str
    user_id: uuid.UUID
    primary: bool = False

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
