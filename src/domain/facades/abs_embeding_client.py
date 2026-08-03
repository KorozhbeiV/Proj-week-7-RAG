from typing import TYPE_CHECKING, Generic, TypeVar
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings

TNativeClient = TypeVar('TNativeClient')



class EmbedClientCreator(ABC, Generic[TNativeClient]):
    def __init__(self, model_name: str | None) -> None:
        self._model_name = model_name

    @staticmethod
    @abstractmethod
    def _create_raw_client() -> TNativeClient:
        ...

    @abstractmethod
    def create_ebmeding_client(self) -> Embeddings:
        ...