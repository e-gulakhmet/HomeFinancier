class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.error = message
        super().__init__(f"{field}: {message}")
