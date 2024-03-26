import pytest

from src.auth_infrastructure.adapters.authorization import JWTAuthorization


@pytest.fixture()
def secret_key() -> str:
    return "dummy_secret_key"


@pytest.fixture()
def algorithm() -> str:
    return "HS256"


@pytest.fixture()
def jwt_authorization(secret_key: str, algorithm: str) -> JWTAuthorization:
    return JWTAuthorization(secret_key=secret_key, algorithm=algorithm)
