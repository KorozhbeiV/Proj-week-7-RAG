from typing import TYPE_CHECKING, Generic, TypeVar, ClassVar, Any
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings

TNativeClient = TypeVar('TNativeClient')



class EmbedClientCreator(ABC, Generic[TNativeClient]):
    registry: ClassVar[dict[str, type[EmbedClientCreator[Any]]]]
    
    def __init__(self, model_name: str | None) -> None:
        self._model_name = model_name

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            EmbedClientCreator.registry[kind] = cls

    @staticmethod
    @abstractmethod
    def _create_raw_client() -> TNativeClient:
        ...

    @abstractmethod
    def create_ebmeding_client(self) -> Embeddings:
        ...