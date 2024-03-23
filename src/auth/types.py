from typing import NewType

Token = NewType("Token", str)

AccessToken = NewType("AccessToken", Token)

RefreshToken = NewType("RefreshToken", Token)
