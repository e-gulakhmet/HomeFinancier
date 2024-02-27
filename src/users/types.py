import re
from typing import NewType
from uuid import UUID

UserID = NewType("UserID", UUID)

HashedPassword = NewType("HashedPassword", bytes)


class Email(str):
    __slots__ = ()

    _EMAIL_PATTERN = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    _INVALID_EMAIL_ERROR_TEXT = "Invalid email address"

    def __new__(cls, address: str) -> "Email":
        if not re.match(cls._EMAIL_PATTERN, address):
            raise ValueError(cls._INVALID_EMAIL_ERROR_TEXT)
        return super().__new__(cls, address)


class Password(str):
    __slots__ = ()

    _MIN_LENGTH = 4
    _MAX_LENGTH = 100
    _MIN_LENGTH_ERROR_TEXT = f"Ensure this value has at least {_MIN_LENGTH} characters"
    _MAX_LENGTH_ERROR_TEXT = f"Ensure this value has at most {_MAX_LENGTH} characters"

    def __new__(cls, password: str) -> "Password":
        if len(password) < cls._MIN_LENGTH:
            raise ValueError(cls._MIN_LENGTH_ERROR_TEXT)
        if len(password) > cls._MAX_LENGTH:
            raise ValueError(cls._MAX_LENGTH_ERROR_TEXT)
        return super().__new__(cls, password)
