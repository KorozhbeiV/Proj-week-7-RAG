from typing import TYPE_CHECKING, Generic, TypeVar, ClassVar, Any
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings
    from src.domain.pipelines.ingestion.protocols.primitive_support_registry import SupportRegistry

TNativeClient = TypeVar('TNativeClient')



class EmbedClientCreator(ABC, Generic[TNativeClient], SupportRegistry):
    registry: ClassVar[dict[str, type[EmbedClientCreator[Any]]]]
    
    def __init__(self, model_name: str | None) -> None:
        ...

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