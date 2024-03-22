import pytest

from src.foundation.password import Password


def test_error_if_password_length_is_less_than_min_length() -> None:
    with pytest.raises(ValueError, match=Password._MIN_LENGTH_ERROR_TEXT):
        Password("1" * (Password._MIN_LENGTH - 1))


def test_error_if_password_length_is_more_than_max_length() -> None:
    with pytest.raises(ValueError, match=Password._MAX_LENGTH_ERROR_TEXT):
        Password("1" * (Password._MAX_LENGTH + 1))
