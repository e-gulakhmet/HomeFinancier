import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    email: str
    password: bytes
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
