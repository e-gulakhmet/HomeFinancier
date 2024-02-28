import uuid

from pytest_mock import MockerFixture

from src.users import UserExistUseCase, UserID


async def test_repo_exists_is_called(usecase: UserExistUseCase, mocker: MockerFixture) -> None:
    user_id = UserID(uuid.uuid4())
    spy = mocker.spy(usecase._user_repo, "exist")

    await usecase.execute(user_id=user_id)

    spy.assert_called_once_with(user_id=user_id)


async def test_bool_is_returned(usecase: UserExistUseCase, mocker: MockerFixture) -> None:
    mocker.patch.object(usecase._user_repo, "exist", return_value=True)

    is_exist = await usecase.execute(user_id=UserID(uuid.uuid4()))

    assert is_exist == usecase._user_repo.exist.return_value  # type: ignore
    assert isinstance(is_exist, bool)
