from abc import abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar
from src.domain.pipelines.ingestion.primitive.facades.abs_main_pipeline_class import IngestionPipeline

if TYPE_CHECKING:
    from pathlib import Path
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.complete.modules.manifest_service.config import PATH_TO_MANIFEST_FILE
    from src.domain.pipelines.ingestion.protocols.primitive_support_registry import SupportRegistry



class ManifestManager(IngestionPipeline, SupportRegistry):
    registry: ClassVar[dict[str, type[ManifestManager]]]

    def __init__(self, db: str | Path | None = None) -> None:
        self.db_path = PATH_TO_MANIFEST_FILE if db is None else Path(db)
        self.db_path.mkdir(parents=True, exist_ok=True)

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            ManifestManager.registry[kind] = cls

    @abstractmethod
    def load_data(self, data: IngestionPipelineContext) -> bool:
        """
        ## Loads new data into manifest.db
        Returns bool whether success
        """
        ...
    
    @abstractmethod
    def init_database(self) -> None:
        ...

    @abstractmethod
    def _update_metadata(self, data: IngestionPipelineContext) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        ...