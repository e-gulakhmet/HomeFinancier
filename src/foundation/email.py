import re


class Email(str):
    __slots__ = ()

    _EMAIL_PATTERN = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    _INVALID_EMAIL_ERROR_TEXT = "Invalid email address"

    def __new__(cls, address: str) -> "Email":
        if not re.match(cls._EMAIL_PATTERN, address):
            raise ValueError(cls._INVALID_EMAIL_ERROR_TEXT)
        return super().__new__(cls, address)
