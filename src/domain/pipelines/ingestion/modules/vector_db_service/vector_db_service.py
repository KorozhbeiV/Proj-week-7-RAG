"""
## Responsible for:
- Reading
- Updating
- Deleting
- Replacing
- Error raising (if any)
in vector DB
"""
from __future__ import annotations
from typing import Any, Self, cast
from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.domain.shared.api_keys import QDRANT_API_KEY, QDRANT_CLASTER_ENDPOINT
from src.domain.shared.config.constants import QDRANT_VECTOR_DB_COLLECTION_NAME
from src.domain.pipelines.ingestion.facades.abs_vector_db_service import VectorDBService
from src.domain.shared.registry.enums import VectorDBServiceKind



class BaseDBService(VectorDBService):
    def __init__(self, store: VectorStore) -> None:
        super().__init__(store)

    @classmethod
    def get_instance(cls, store: VectorStore) -> Self:
        if cls._instance is None:
            cls._instance = cls(store)
        return cast(Self, cls._instance)    



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
        return cls.get_instance(store)


    def read_db(self, query: str, k: int) -> list[Document]:
        return self._store.similarity_search(query=query, k=k)


    def update_db(self, texts: list[str], metadatas: list[dict[str, Any]]) -> list[str | int]:
        store = cast(QdrantVectorStore, self._store)
        # The library does not provide enough stabs
        return store.add_texts(texts=texts, metadatas=metadatas) #pyright: ignore


    def delete_from_db(self, ids: list[str | int]) -> bool:
        store = cast(QdrantVectorStore, self._store)
        if (result := store.delete(ids)) is None:
            result = False
        return result


    def replace_in_db(self,
                    ids: list[str | int],
                    new_texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        """
        ## Syntax-sugar-method
        - Uses both, `delete_from_db` and `update_db` methods
        - It's possible to process the same action by calling these two method directly
        """
        self.delete_from_db(ids)
        return self.update_db(new_texts, metadatas)
