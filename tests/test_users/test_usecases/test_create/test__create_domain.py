from src.users.entities import User
from src.users.usecases import UserCreateInput, UserCreateUseCase


async def test_domain_entity_is_created(usecase: UserCreateUseCase, input_: UserCreateInput) -> None:
    user = usecase._create_domain(input_)

    assert isinstance(user, User)
    assert user.email == input_.email
    assert user.password == usecase._hashing_provider.hash_password.return_value # type: ignore
