from typing import ClassVar, Any, Self, TYPE_CHECKING
from abc import abstractmethod
from src.domain.pipelines.ingestion.primitive.orcestration.abs_main_pipeline_class import IngestionPipeline

if TYPE_CHECKING:
    from langchain_core.vectorstores import VectorStore
    from langchain_core.embeddings import Embeddings
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.complete.facades.abs_hashing_service import HashingService



class VectorDBService(IngestionPipeline):
    """
    ### Use method `create` to init this class
    """
    registry: ClassVar[dict[str, type[VectorDBService]]]
    _instance: ClassVar[VectorDBService | None]
    _store: VectorStore
    

    def __init__(self, store : VectorStore, hasher: type[HashingService]) -> None:
        self._store = store
        self._hasher = hasher()


    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._instance = None
        if kind is not None:
            VectorDBService.registry[kind] = cls

    @classmethod
    @abstractmethod
    def _get_instance(cls, store: VectorStore, hasher: type[HashingService]) -> Self:
        ...

    @abstractmethod
    @staticmethod
    def _get_metadata_for_chunks(data: IngestionPipelineContext) -> list[dict[str, Any]]:
        ...
    
    @abstractmethod
    @staticmethod
    def _get_ids_to_delete(metadatas: list[dict[str, Any]]) -> list[str | int]:
        ...

    @abstractmethod
    def perform_action_over_files(self, data: IngestionPipelineContext) -> dict[str, Any]:
        ...

    @classmethod
    @abstractmethod
    def create(cls, embeding_model: Embeddings, hasher: type[HashingService]) -> Self:
        ...

    @abstractmethod
    def add_to_db(self,
                    texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        ...

    @abstractmethod
    def delete_from_db(self, ids: list[str | int]) -> bool:
        ...

    @abstractmethod
    def update_db(self,
                    ids: list[str | int],
                    new_texts: list[str],
                    metadatas: list[dict[str, Any]]
                    ) -> list[str | int]:
        """
        ## Syntax-sugar-method
        - Uses both, `delete_from_db` and `add_to_db` methods
        - It's possible to process the same action by calling these two method directly
        """
        ...
    