from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from pathlib import Path
    from langchain_core.embeddings import Embeddings



class ChunkingService(ABC):
    def __init__(self, embeding_model: Embeddings) -> None:
        self._embeding_model = embeding_model

    @staticmethod
    @abstractmethod
    def read_file(file: Path) -> str:
        ...
        
    @abstractmethod
    def split_on_chunks(self,
                        text: str,
                        ) -> list[str]:
        ...