import re
from typing import NewType
from uuid import UUID


class StorageLink(str):
    __slots__ = ()

    _GOOGLE_SHEETS_LINK_PATTERN = r"https:\/\/docs\.google\.com\/spreadsheets\/d\/[a-zA-Z0-9_-]+"
    _INVALID_LINK_ERROR_TEXT = "Storage link is invalid"

    def __new__(cls, value: str) -> "StorageLink":
        if not re.match(pattern=cls._GOOGLE_SHEETS_LINK_PATTERN, string=value):
            raise ValueError(cls._INVALID_LINK_ERROR_TEXT)
        return super().__new__(cls, value)


StorageID = NewType("StorageID", UUID)

OwnerID = NewType("OwnerID", UUID)
