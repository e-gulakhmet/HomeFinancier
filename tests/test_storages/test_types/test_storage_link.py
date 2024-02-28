import pytest

from src.storages import StorageLink


@pytest.mark.parametrize(
    "link_address",
    [
        "https://docs.google.com/spreadsheets/d/1",
        "https://docs.google.com/spreadsheets/d/1/edit",
        "https://docs.google.com/spreadsheets/d/1/edit#gid=0",
    ],
)
def test_storage_link_is_created_successfully(link_address: str) -> None:
    StorageLink(link_address)


@pytest.mark.parametrize(
    "link_address",
    [
        "https://www.example.com/spreadsheets/d/1",
        "https://reddit.com/neovim",
        "https://google.com",
    ],
)
def test_error_if_storage_link_is_invalid(link_address: str) -> None:
    with pytest.raises(ValueError, match=StorageLink._INVALID_LINK_ERROR_TEXT):
        StorageLink(link_address)
