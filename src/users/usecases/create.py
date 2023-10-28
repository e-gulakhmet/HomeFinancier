import abc
import re
from dataclasses import dataclass

from src.exceptions.core import ValidationError
from src.users.entities import User


class UserCreateRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def exists(self, email: str) -> bool:
        ...

    @abc.abstractmethod
    async def save(self, user: User) -> None:
        ...


class UserCreateHashingProviderInterface(abc.ABC):
    @abc.abstractmethod
    def hash_password(self, password: str) -> bytes:
        ...


@dataclass
class UserCreateUseCaseValidationRules:
    password_min_length: int


@dataclass
class UserCreateInput:
    email: str
    password: str


class UserCreateUseCase:
    def __init__(
            self,
            user_repo: UserCreateRepoInterface,
            hashing_provider: UserCreateHashingProviderInterface,
            validation_rules: UserCreateUseCaseValidationRules,
        ) -> None:
        self._user_repo = user_repo
        self._hashing_provider = hashing_provider
        self._validation_rules = validation_rules

    async def execute(self, input_: UserCreateInput) -> User:
        await self._validate(input_=input_)

        user = self._create_domain(input_=input_)

        await self._user_repo.save(user=user)

        return user

    async def _validate(self, input_: UserCreateInput) -> None:
        await self._validate_email(email=input_.email)
        self._validate_password(password=input_.password)

    async def _validate_email(self, email: str) -> None:
        if not self._is_correct_email_format(email=email):
            raise ValidationError(field="email", message="Invalid email")

        if await self._user_repo.exists(email=email):
            raise ValidationError(field="email", message="Email already exists")

    def _is_correct_email_format(self, email: str) -> bool:
        if (
            not email
            or not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        ):
            return False
        return True

    def _validate_password(self, password: str) -> None:
        if not password:
            raise ValidationError(field="password", message="Field is required")
        if len(password) < self._validation_rules.password_min_length:
            raise ValidationError(
                field="password",
                message=f"Password must be at least {self._validation_rules.password_min_length} characters"
            )

    def _create_domain(self, input_: UserCreateInput) -> User:
        hashed_password = self._hashing_provider.hash_password(input_.password)
        return User(
            email=input_.email,
            password=hashed_password,
        )
