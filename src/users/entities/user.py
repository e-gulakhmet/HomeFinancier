from dataclasses import dataclass
from datetime import datetime

from src.foundation.email import Email
from src.users.types import HashedPassword, UserID


@dataclass
class User:
    id: UserID
    created_at: datetime
    updated_at: datetime
    email: Email
    password: HashedPassword
