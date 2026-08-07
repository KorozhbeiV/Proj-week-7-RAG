from pathlib import Path
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from src.domain.pipelines.ingestion.facades.abs_chunking_service import ChunkingService
from src.domain.shared.registry.enums import ChunkingServiceKind



class BaseChunkingService(ChunkingService):
    def __init__(self, embeding_model: Embeddings) -> None:
        super().__init__(embeding_model)
    
    @staticmethod
    def read_file(file: Path) -> str:
        with open(file, "r", encoding='utf-8') as f:
            return f.read()



class EmbedingChunkingService(BaseChunkingService, kind=ChunkingServiceKind.EMBEDING_CHUNKING_SERVICE.value):
    def split_on_chunks(self,
                        text: str,
                        ) -> list[str]:
        splitter = SemanticChunker(embeddings=self._embeding_model)
        return splitter.split_text(text)

