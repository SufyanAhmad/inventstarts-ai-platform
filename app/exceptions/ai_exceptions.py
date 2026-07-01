class AIProviderException(Exception):

    def __init__(
        self,
        message: str = "AI provider is temporarily unavailable.",
        error_code: str = "AI_PROVIDER_ERROR",
        status_code: int = 503
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)