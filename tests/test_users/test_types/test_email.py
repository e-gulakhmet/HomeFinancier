import pytest

from src.users import Email


def test_error_if_email_is_invalid() -> None:
    with pytest.raises(ValueError, match=Email._INVALID_EMAIL_ERROR_TEXT):
        Email("invalid-email")
