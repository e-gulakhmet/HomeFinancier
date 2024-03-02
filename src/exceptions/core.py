class ValidationError(Exception):
    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        self.error = message
        if field is None:
            super().__init__(message)
        else:
            super().__init__(f"{field}: {message}")
