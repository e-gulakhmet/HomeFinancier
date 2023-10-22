import pytest

from src.users.usecases import UserCreateUseCase


@pytest.mark.parametrize(("email", "valid"), [
    ("invalid_email", False),
    ("", False),
    ("example@gmail.com", True),
])
def test_error_if_email_is_invalid(usecase: UserCreateUseCase, email: str, valid: bool) -> None:
    assert usecase._is_correct_email_format(email) == valid
