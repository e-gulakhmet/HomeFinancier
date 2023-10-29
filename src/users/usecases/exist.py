import abc
import uuid


class UserExistRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def exist(self, user_id: uuid.UUID) -> bool:
        ...

class UserExistUseCase:
    def __init__(self, user_repo: UserExistRepositoryInterface) -> None:
        self._user_repo = user_repo

    async def execute(self, user_id: uuid.UUID) -> bool:
        return self._user_repo.exist(user_id=user_id)
