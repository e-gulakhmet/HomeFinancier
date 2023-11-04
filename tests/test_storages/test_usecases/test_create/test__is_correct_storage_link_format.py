# pyright: reportPrivateUsage=false

import pytest

from src.storages.usecases import StorageCreateUseCase


@pytest.mark.parametrize(("storage_link", "valid"), [
    ("some_text", False),
    ("", False),
    ("https://www.fake_storage.com/123456789", False),
    ("https://docs.google.com/spreadsheets/d/18nSstUo7EaCLAVZ", True),
], ids=["some_text", "empty", "random_link", "google_sheets_link"])
def test_error_if_storage_link_is_invalid(usecase: StorageCreateUseCase, storage_link: str, valid: bool) -> None:
    assert usecase._is_correct_storage_link_format(link=storage_link) == valid
