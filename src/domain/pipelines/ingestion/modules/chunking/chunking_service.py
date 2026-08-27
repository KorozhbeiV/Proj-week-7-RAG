from pathlib import Path
from dataclasses import replace
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from src.domain.pipelines.ingestion.facades.abs_chunking_service import ChunkingService
from src.domain.shared.registry.enums import ChunkingServiceKind
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext



class BaseChunkingService(ChunkingService):
    def __init__(self, embeding_model: Embeddings) -> None:
        super().__init__(embeding_model)
        self._chunking_type: str = ''
    
    @staticmethod
    def read_file(file: Path) -> str:
        with open(file, "r", encoding='utf-8') as f:
            return f.read()
    
    
    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        assert data.f_path is not None
        read = self.read_file(data.f_path)
        chunks, chunk_count, chinking_type = self.split_on_chunks(read)
        assert not isinstance(data, type)
        return replace(data, chunks=chunks, chunk_count=chunk_count, chinking_type=chinking_type)



class EmbedingChunkingService(BaseChunkingService, kind=ChunkingServiceKind.EMBEDING_CHUNKING_SERVICE.value):
    def split_on_chunks(self, text: str) -> tuple[list[str], int, str]:
        splitter = SemanticChunker(embeddings=self._embeding_model,
                                    breakpoint_threshold_type='percentile',
                                    breakpoint_threshold_amount=90)
        chunks = splitter.split_text(text)
        setattr(self, self._chunking_type, ChunkingServiceKind.EMBEDING_CHUNKING_SERVICE.value)
        return chunks, len(chunks), self._chunking_type