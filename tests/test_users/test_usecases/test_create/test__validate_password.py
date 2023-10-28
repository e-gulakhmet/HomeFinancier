import pytest

from src.exceptions import ValidationError
from src.users.usecases import UserCreateUseCase


@pytest.mark.parametrize(("password", "error_message"), [
    ("", "Field is required"),
    ("123", "Password must be at least 4 characters"),
])
def test_error_if_password_is_invalid(usecase: UserCreateUseCase, password: str, error_message: str) -> None:
    with pytest.raises(ValidationError, match=f"password: {error_message}") as exc:
        usecase._validate_password(password)
    assert exc.value.field == "password"
    assert exc.value.error == error_message


@pytest.mark.parametrize("password", [
    "1234",
])
def test_no_error_if_password_is_valid(usecase: UserCreateUseCase, password: str) -> None:
    try:
        usecase._validate_password(password)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
