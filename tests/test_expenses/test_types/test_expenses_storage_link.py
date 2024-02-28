import pytest

from src.expenses import ExpensesStorageLink


@pytest.mark.parametrize(
    "link_address",
    [
        "https://docs.google.com/spreadsheets/d/1",
        "https://docs.google.com/spreadsheets/d/1/edit",
        "https://docs.google.com/spreadsheets/d/1/edit#gid=0",
        "https://docs.google.com/spreadsheets/d/1/edit#gid=0&vpid=1",
    ],
)
def test_expenses_storage_link_is_created_successfully(link_address: str) -> None:
    try:
        ExpensesStorageLink(link_address)
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
def test_error_if_expenses_storage_link_is_invalid(link_address: str) -> None:
    with pytest.raises(ValueError, match=ExpensesStorageLink._INVALID_LINK_ERROR_TEXT):
        ExpensesStorageLink(link_address)
