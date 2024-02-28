import re
from typing import NewType
from uuid import UUID

OwnerID = NewType("OwnerID", UUID)


class ExpensesStorageLink(str):
    __slots__ = ()

    _GOOGLE_SHEETS_LINK_PATTERN = r"https:\/\/docs\.google\.com\/spreadsheets\/d\/[a-zA-Z0-9_-]+"
    _INVALID_LINK_ERROR_TEXT = "Expenses Storage link is invalid"

    def __new__(cls, value: str) -> "ExpensesStorageLink":
        if not re.match(pattern=cls._GOOGLE_SHEETS_LINK_PATTERN, string=value):
            raise ValueError(cls._INVALID_LINK_ERROR_TEXT)
        return super().__new__(cls, value)


class Amount(float):
    _AMOUNT_MIN_VALUE_ERROR_MESSAGE = "Amount cannot be negative"

    def __new__(cls, value: float) -> "Amount":
        if value <= 0:
            raise ValueError(cls._AMOUNT_MIN_VALUE_ERROR_MESSAGE)
        return super().__new__(cls, value)


class Category(str):
    __slots__ = ()

    _CATEGORY_MAX_LENGTH = 50
    _CATEGORY_MIN_LENGTH = 3
    _CATEGORY_LENGTH_ERROR_MESSAGE = (
        f"Category must be between {_CATEGORY_MIN_LENGTH} and {_CATEGORY_MAX_LENGTH} characters"
    )

    def __new__(cls, value: str) -> "Category":
        if not cls._CATEGORY_MIN_LENGTH <= len(value) <= cls._CATEGORY_MAX_LENGTH:
            raise ValueError(cls._CATEGORY_LENGTH_ERROR_MESSAGE)
        return super().__new__(cls, value)
