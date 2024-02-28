import pytest
from pytest_mock import MockerFixture

from src.exceptions import ValidationError
from src.users import User, UserCreateInput, UserCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(usecase: UserCreateUseCase, mocker: MockerFixture) -> None:
    mocker.patch.object(usecase._user_repo, "exists", return_value=False)


async def test_error_if_email_already_exists(
    usecase: UserCreateUseCase,
    input_: UserCreateInput,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(usecase._user_repo, "exists", return_value=True)

    with pytest.raises(ValidationError, match="email: Email already exists"):
        await usecase.execute(input_)


async def test_user_is_saved_to_repository(
    usecase: UserCreateUseCase, input_: UserCreateInput, mocker: MockerFixture,
) -> None:
    spy = mocker.spy(usecase._user_repo, "save")

    await usecase.execute(input_)

    saved_user = User(
        id=mocker.ANY,
        email=input_.email,
        password=usecase._hashing_provider.hash_password.return_value,  # type: ignore
        created_at=mocker.ANY,
        updated_at=mocker.ANY,
    )

    spy.assert_called_once_with(saved_user)


async def test_user_entity_is_returned(usecase: UserCreateUseCase, input_: UserCreateInput) -> None:
    user = await usecase.execute(input_)

    assert isinstance(user, User)
