from src.foundation.password import Password
from src.users import HashedPassword


class FakeHashingAdapter:
    async def hash_password(self, password: Password) -> HashedPassword:
        return HashedPassword(password.encode())

    async def verify_password(self, password: Password, hashed_password: HashedPassword) -> bool:
        return password.encode() == hashed_password
