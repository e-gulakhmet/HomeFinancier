from unittest.mock import Mock

from src.foundation.password import Password
from src.users import User, UserVerifyPasswordInput, UserVerifyPasswordUseCase


async def test_true_is_returned_if_user_exists_and_passed_password_matches(
    user_verify_password_usecase: UserVerifyPasswordUseCase,
    users_repository_mock: Mock,
    hashing_mock: Mock,
    user: User,
) -> None:
    users_repository_mock.get.return_value = user
    hashing_mock.verify_password.return_value = True

    output = await user_verify_password_usecase.execute(
        UserVerifyPasswordInput(
            user_id=user.id,
            password=Password("example_password"),
        ),
    )

    assert output is True


async def test_false_is_returned_if_user_does_not_exist(
    user_verify_password_usecase: UserVerifyPasswordUseCase,
    users_repository_mock: Mock,
    user: User,
) -> None:
    users_repository_mock.get.return_value = None

    output = await user_verify_password_usecase.execute(
        UserVerifyPasswordInput(
            user_id=user.id,
            password=Password("example_password"),
        ),
    )

    assert output is False


async def test_false_is_returned_if_user_exists_but_passed_password_does_not_match_user_password(
    user_verify_password_usecase: UserVerifyPasswordUseCase,
    users_repository_mock: Mock,
    hashing_mock: Mock,
    user: User,
) -> None:
    users_repository_mock.get.return_value = user
    hashing_mock.verify_password.return_value = False

    output = await user_verify_password_usecase.execute(
        UserVerifyPasswordInput(
            user_id=user.id,
            password=Password("example_password"),
        ),
    )

    assert output is False
