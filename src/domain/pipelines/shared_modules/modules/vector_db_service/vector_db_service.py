"""
## Responsible for:
- Updating
- Deleting
- Replacing
- Error raising (if any)
in the given vector DB
"""
from typing import Any, Self, cast, Iterator
from dataclasses import replace, fields
from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.shared.logger_config import logger
from src.domain.shared.api_keys import QDRANT_API_KEY, QDRANT_CLASTER_ENDPOINT
from src.domain.shared.config.constants import QDRANT_VECTOR_DB_COLLECTION_NAME
from src.domain.pipelines.shared_modules.facades.abs_vector_db_service import VectorDBService
from src.domain.pipelines.ingestion.pipeline_entities.registry_enums import VectorDBServiceKind
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status



class BaseDBService(VectorDBService):
    def __init__(self, store: VectorStore) -> None:
        super().__init__(store)

    @classmethod
    def _get_instance(cls, store: VectorStore) -> Self:
        if cls._instance is None:
            cls._instance = cls(store)
        return cast(Self, cls._instance)
    
    @staticmethod
    def _get_ids_to_delete(metadatas: dict[str, dict[str, Any] | list[dict[str, Any]]]) -> list[str | int]:
        chunks = cast(list[dict[str, Any]], metadatas['chunks'])
        return [el["chunk_ids"] for el in chunks]
    
    @staticmethod
    def _get_metadata_for_chunks(data: IngestionPipelineContext) -> list[dict[str, Any]]:
        assert (chunks := data.text_chunk) is not None
        file_level = {f"{f.name}": getattr(data, f.name) for
                        f in
                        fields(data) if
                        f.metadata.get('chunk_metadata') # <- bool value
                        }
        return [{**file_level, 'chunk_index': idx} for
                idx, _ in
                enumerate(chunks)
                ]
    
    @staticmethod
    def _batched(texts: list[str], metadatas: list[dict[str, Any]], size: int = 20) -> Iterator[tuple[list[str], list[dict[str, Any]]]]:
        total_chunks = len(texts)
        if size > total_chunks:
            size = total_chunks
        logger.debug(f"Batch size: '{size}'")
        already_processed: int = 0
        for i in range(0, total_chunks, size):
            logger.debug(f"Loading chunks... Chunks left: '{total_chunks - already_processed}'")
            already_processed = i + size
            yield texts[i:i + size], metadatas[i:i + size]
            

    
    def perform_action_over_files(self, data: IngestionPipelineContext) -> dict[str, Any]:
        assert (action := data.action) is not None

        if action == Action.DELETED:
            assert (md := data.file_metadata) # Is not an empty list
            ids_to_delete = self._get_ids_to_delete(md)
            return {"chunks_deleted": self.delete_from_db(ids_to_delete),
                    "chunk_ids": [],
                    "delete_record_for_file": True
                    }
        assert (texts := data.text_chunk) is not None
        metadatas = self._get_metadata_for_chunks(data)
        if action == Action.ADDED:
            chunk_ids: list[str | int] = []
            for c, m in self._batched(texts, metadatas):
                chunk_ids.extend(self.add_to_db(c, m))
            return {"chunk_ids": chunk_ids,
                    "chunks_deleted": None
                    }
        raise RuntimeError(f"No action was performed over the given file: '{data.f_path}'")


    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        performed = self.perform_action_over_files(data)
        performed.update({"status": Status.VBD_UPDATED})
        result = replace(data, **performed)
        self._log_changes(result)
        return result



class QdrantDBService(BaseDBService, kind=VectorDBServiceKind.QDRANT_DB_SERVICE.value):
    @classmethod
    def create(cls, embeding_model: Embeddings) -> Self:
        client = QdrantClient(
                        url=QDRANT_CLASTER_ENDPOINT,
                        api_key=QDRANT_API_KEY,
                        timeout=100
                        )
        if not client.collection_exists(QDRANT_VECTOR_DB_COLLECTION_NAME):
            client.create_collection(
                collection_name=QDRANT_VECTOR_DB_COLLECTION_NAME,
                vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
                )
        store = QdrantVectorStore(
                    client=client,
                    collection_name=QDRANT_VECTOR_DB_COLLECTION_NAME,
                    embedding=embeding_model,
                )
        return cls._get_instance(store)


    def add_to_db(self,
                    texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        store = cast(QdrantVectorStore, self._store)
        # The library does not provide enough stabs
        return store.add_texts(texts=texts, metadatas=metadatas) #pyright: ignore


    def delete_from_db(self, ids: list[str | int]) -> bool:
        store = cast(QdrantVectorStore, self._store)
        if (result := store.delete(ids)) is None:
            result = False
        return result


    def update_db(self,
                    ids: list[str | int],
                    new_texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        self.delete_from_db(ids)
        return self.add_to_db(new_texts, metadatas)
