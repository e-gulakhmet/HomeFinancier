import pytest

from src.transactions import Category


@pytest.mark.parametrize(
    "category_name",
    [
        "Food",
        "Entertainment",
    ],
)
def test_category_is_created_successfully(category_name: str) -> None:
    try:
        Category(category_name)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


@pytest.mark.parametrize(
    "category_name",
    [
        "F",
        "EntertainmentEntertainmentEntertainmentEntertainmentEntertainmentEntertainmentEntertainment",
    ],
)
def test_error_if_category_length_is_invalid(category_name: str) -> None:
    with pytest.raises(ValueError, match=Category._CATEGORY_LENGTH_ERROR_MESSAGE):
        Category(category_name)
