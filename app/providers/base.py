from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @abstractmethod
    async def generate_response(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        pass
