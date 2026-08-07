from typing import TYPE_CHECKING, overload
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings



class EmbedingProcessor(ABC):
    def __init__(self, embeding_model: Embeddings) -> None:
        self.embeding_model = embeding_model

    @overload
    def to_embedings(self, text: str) -> list[float]: ...

    @overload
    def to_embedings(self, text: list[str]) -> list[list[float]]: ...

    @abstractmethod
    def to_embedings(self, text: str | list[str]) -> list[float] | list[list[float]]:
        ...