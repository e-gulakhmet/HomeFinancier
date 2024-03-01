import pytest

from src.transactions import StorageLink


@pytest.mark.parametrize(
    "link_address",
    [
        "https://docs.google.com/spreadsheets/d/1",
        "https://docs.google.com/spreadsheets/d/1/edit",
        "https://docs.google.com/spreadsheets/d/1/edit#gid=0",
        "https://docs.google.com/spreadsheets/d/1/edit#gid=0&vpid=1",
    ],
)
def test_storage_link_is_created_successfully(link_address: str) -> None:
    try:
        StorageLink(link_address)
    except Exception as e:
        msg = f"Unexpected error: {e}"
        pytest.fail(msg)


@pytest.mark.parametrize(
    "link_address",
    [
        "https://www.google.com",
        "https://www.example.com/spreadsheets/d/1",
    ],
)
def test_error_if_storage_link_is_invalid(link_address: str) -> None:
    with pytest.raises(ValueError, match=StorageLink._INVALID_LINK_ERROR_TEXT):
        StorageLink(link_address)
