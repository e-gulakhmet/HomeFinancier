import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Expense:
    user_id: uuid.UUID
    exepenses_storage_link: str
    amount: float
    category: str
    subcategory: str = ""
    created_at: datetime = field(default_factory=datetime.now)
