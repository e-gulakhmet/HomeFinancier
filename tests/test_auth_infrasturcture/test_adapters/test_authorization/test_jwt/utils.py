from typing import Any

import jwt

from src.auth import Token


def decode_token(token: Token, secret_key: str, algorithm: str) -> dict[str, Any]:
    return jwt.decode(token, secret_key, algorithms=[algorithm])  # type: ignore


def encode_token(payload: dict[str, Any], secret_key: str, algorithm: str) -> Token:
    return Token(jwt.encode({**payload}, secret_key, algorithm))
