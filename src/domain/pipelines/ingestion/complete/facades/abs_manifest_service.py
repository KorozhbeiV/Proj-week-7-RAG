from abc import abstractmethod
from typing import TYPE_CHECKING, Any
from src.domain.pipelines.ingestion.primitive.orcestration.abs_main_pipeline_class import IngestionPipeline

if TYPE_CHECKING:
    from pathlib import Path
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.complete.modules.manifest_service.config import PATH_TO_MANIFEST_FILE



class ManifestManager(IngestionPipeline):
    def __init__(self, db: str | Path | None = None) -> None:
        self.db_path = PATH_TO_MANIFEST_FILE if db is None else Path(db)
        self.db_path.mkdir(parents=True, exist_ok=True)

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