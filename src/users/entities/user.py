import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.users.types import Email, HashedPassword, UserID


@dataclass
class User:
    email: Email
    password: HashedPassword
    id: UserID = field(default_factory=lambda: UserID(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
