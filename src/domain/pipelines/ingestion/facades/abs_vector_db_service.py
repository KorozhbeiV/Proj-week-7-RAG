from abc import ABC, abstractmethod
from typing import ClassVar, Any, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore
    from langchain_core.embeddings import Embeddings
    from langchain_core.documents import Document



class VectorDBService(ABC):
    registry: ClassVar[dict[str, type[VectorDBService]]]
    _instance: ClassVar[VectorDBService | None]
    _store: VectorStore
    

    def __init__(self, store : VectorStore) -> None:
        self._store = store


    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._instance = None
        if kind is not None:
            VectorDBService.registry[kind] = cls

    @classmethod
    @abstractmethod
    def get_instance(cls, store: VectorStore) -> Self:
        ...

    @classmethod
    @abstractmethod
    def create(cls, embeding_model: Embeddings) -> Self:
        ...

    @abstractmethod
    def read_db(self, query: str, k: int) -> list[Document]:
        ...

    @abstractmethod
    def update_db(self,
                    texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        ...
    
    @abstractmethod
    def delete_from_db(self, ids: list[str | int]) -> bool:
        ...

    @abstractmethod
    def replace_in_db(self,
                    ids: list[str | int],
                    new_texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        ...
    