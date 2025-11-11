class DataAccessException(Exception):

    def __init__(self, message: str, *, error_code: str = "DATA_ACCESS_ERROR", details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        base = f"{self.error_code}: {self.message}"
        if self.details:
            return f"{base} | details={self.details}"
        return base
