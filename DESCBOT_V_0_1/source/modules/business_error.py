class BusinessError(Exception):
    """Exceção personalizada para erros de negócio."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message