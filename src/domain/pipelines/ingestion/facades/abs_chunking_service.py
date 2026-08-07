from typing import TYPE_CHECKING, Any, ClassVar
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from pathlib import Path
    from langchain_core.embeddings import Embeddings



class ChunkingService(ABC):
    registry: ClassVar[dict[str, type[ChunkingService]]]

    def __init__(self, embeding_model: Embeddings) -> None:
        self._embeding_model = embeding_model

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            ChunkingService.registry[kind] = cls

    @staticmethod
    @abstractmethod
    def read_file(file: Path) -> str:
        ...
        
    @abstractmethod
    def split_on_chunks(self,
                        text: str,
                        ) -> list[str]:
        ...