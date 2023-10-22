import pytest
from pytest_mock import MockerFixture

from src.exceptions import ValidationError
from src.users.usecases import UserCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture, usecase: UserCreateUseCase) -> None:
    mocker.patch.object(usecase, "_is_correct_email_format", return_value=True)
    mocker.patch.object(usecase._user_repo, "exists", return_value=False)


class TestValidatingEmailFormat:
    async def test__is_correct_email_format_called(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        email = "example@email.com"
        spy = mocker.spy(usecase, "_is_correct_email_format")

        await usecase._validate_email(email=email)

        spy.assert_called_once_with(email=email)

    async def test_error_if_email_is_invalid(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase, "_is_correct_email_format", return_value=False)

        with pytest.raises(ValidationError, match="email: Invalid email") as exc:
            await usecase._validate_email(email="example@email.com")
        assert exc.value.field == "email"
        assert exc.value.error == "Invalid email"

    async def test_no_error_if_email_is_valid(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase, "_is_correct_email_format", return_value=True)

        try:
            await usecase._validate_email(email="example@gmail.com")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")


class TestValidatingEmailUniqueness:
    async def test_repo_exists_called(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        email = "example@email.com"
        spy = mocker.spy(usecase._user_repo, "exists")

        await usecase._validate_email(email=email)

        spy.assert_called_once_with(email=email)

    async def test_error_if_email_already_exists(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._user_repo, "exists", return_value=True)

        with pytest.raises(ValidationError, match="email: Email already exists") as exc:
            await usecase._validate_email(email="example@email.com")
        assert exc.value.error == "Email already exists"
        assert exc.value.field == "email"

    async def test_no_error_if_email_does_not_exist(
            self, usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._user_repo, "exists", return_value=False)

        try:
            await usecase._validate_email(email="example@email.com")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")
