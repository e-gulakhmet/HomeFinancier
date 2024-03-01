from dataclasses import dataclass
from datetime import datetime

from src.users.types import Email, HashedPassword, UserID


@dataclass
class User:
    id: UserID
    created_at: datetime
    updated_at: datetime
    email: Email
    password: HashedPassword
