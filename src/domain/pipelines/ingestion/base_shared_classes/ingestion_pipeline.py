from dataclasses import fields
from src.shared.logger_config import logger
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.shared_abstracts.abs_ingestion_pipeline import IngestionPipeline



class BaseIngestionPipeline(IngestionPipeline):
    @staticmethod
    def _log_changes(data: IngestionPipelineContext) -> None:
        populated = [f"{f.name}: {getattr(data, f.name)}" for
                    f in fields(data) if
                    getattr(data, f.name) is not None and
                    getattr(data, f.name) != []
                    ]
        logger.debug(f"Module passed successfully. Data:\n    {'\n    '.join(populated)}")