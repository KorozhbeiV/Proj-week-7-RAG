"""
## Responsible for:
- Updating
- Deleting
- Replacing
- Error raising (if any)
in the given vector DB
"""
from typing import Any, Self, cast
from dataclasses import replace, fields
from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.domain.shared.api_keys import QDRANT_API_KEY, QDRANT_CLASTER_ENDPOINT
from src.domain.shared.config.constants import QDRANT_VECTOR_DB_COLLECTION_NAME
from src.domain.pipelines.ingestion.primitive.facades.abs_vector_db_service import VectorDBService
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
    def _get_ids_to_delete(metadatas: list[dict[str, Any]]) -> list[str | int]:
        return [el['chunk_ids'] for el in metadatas]
    
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

    
    def perform_action_over_files(self, data: IngestionPipelineContext) -> dict[str, Any]:
        assert (action := data.action) is not None
        assert (md := data.chunk_metadata) # Is not an empty list

        if action == Action.DELETED:
            ids_to_delete = self._get_ids_to_delete(md)
            return {"chunks_deleted": self.delete_from_db(ids_to_delete),
                    "chunks_ids": []
                    }
        assert (chunks := data.text_chunk) is not None
        metadatas = self._get_metadata_for_chunks(data)
        if action == Action.UPDATED:
            ids_to_delete = self._get_ids_to_delete(md)
            return {"chunks_ids": self.update_db(ids_to_delete, chunks, metadatas),
                    "chunks_deleted": None
                    }
        if action == Action.ADDED:
            return {"chunks_ids": self.add_to_db(chunks, metadatas),
                    "chunks_deleted": None
                    }
        raise RuntimeError(f"No action was performed over the given file: '{data.f_path}'")


    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        performed = self.perform_action_over_files(data)
        performed.update({"status": Status.VBD_UPDATED})
        return replace(data, **performed)



class QdrantDBService(BaseDBService, kind=VectorDBServiceKind.QDRANT_DB_SERVICE.value):
    @classmethod
    def create(cls, embeding_model: Embeddings) -> Self:
        client = QdrantClient(
                        url=QDRANT_CLASTER_ENDPOINT,
                        api_key=QDRANT_API_KEY
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
