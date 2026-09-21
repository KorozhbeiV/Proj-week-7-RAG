from typing import TYPE_CHECKING, Any, ClassVar
from abc import abstractmethod
from src.domain.pipelines.ingestion.base_shared_classes.ingestion_pipeline import BaseIngestionPipeline
from src.domain.pipelines.ingestion.protocols.primitive_support_registry import SupportRegistry

if TYPE_CHECKING:
    from pathlib import Path
    from langchain_core.embeddings import Embeddings



class ChunkingService(BaseIngestionPipeline, SupportRegistry):
    registry: ClassVar[dict[str, type[ChunkingService]]] = {}

    def __init__(self, embeding_model: Embeddings) -> None:
        self._embeding_model = embeding_model
        self._chunking_type: str

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            ChunkingService.registry[kind] = cls

    @staticmethod
    @abstractmethod
    def read_file(file: Path) -> str:
        ...
        
    @abstractmethod
    def split_on_chunks(self, text: str) -> tuple[list[str], int, str]:
        """
        ## Returns:
        - list of str chunks
        - number of chunks
        - type of chunking
        """
        ...