import pytest

from src.expenses import Amount


@pytest.mark.parametrize(
    "amount",
    [
        1,
        100,
    ],
)
def test_amount_is_created_successfully(amount: int) -> None:
    try:
        Amount(amount)
    except Exception as e:
        msg = f"Unexpected error: {e}"
        pytest.fail(msg)


@pytest.mark.parametrize(
    "amount",
    [
        0,
        -1,
    ],
)
def test_error_if_amount_is_less_than_min_value(amount: int) -> None:
    with pytest.raises(ValueError, match=Amount._AMOUNT_MIN_VALUE_ERROR_MESSAGE):
        Amount(amount)
