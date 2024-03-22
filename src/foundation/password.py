class Password(str):
    __slots__ = ()

    _MIN_LENGTH = 4
    _MAX_LENGTH = 100
    _MIN_LENGTH_ERROR_TEXT = f"Ensure this value has at least {_MIN_LENGTH} characters"
    _MAX_LENGTH_ERROR_TEXT = f"Ensure this value has at most {_MAX_LENGTH} characters"

    def __new__(cls, password: str) -> "Password":
        if len(password) < cls._MIN_LENGTH:
            raise ValueError(cls._MIN_LENGTH_ERROR_TEXT)
        if len(password) > cls._MAX_LENGTH:
            raise ValueError(cls._MAX_LENGTH_ERROR_TEXT)
        return super().__new__(cls, password)
