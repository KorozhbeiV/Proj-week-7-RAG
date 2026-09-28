from dataclasses import fields
from src.shared.logger_config import logger
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.shared_abstracts.abs_ingestion_pipeline import IngestionPipeline



class BaseIngestionPipeline(IngestionPipeline):
    @staticmethod
    def __shorten_values_to_log(populated: list[str], len_for_el: int) -> list[str]:
        shorten: list[str] = []
        for el in populated:
            if len(el) < len_for_el:
                shorten.append(el)
            else:
                shorten.append(f'{el[:len_for_el]}...')
        return shorten


    def _log_changes(self, data: IngestionPipelineContext) -> None:
        populated = [f"{f.name}: {getattr(data, f.name)}" for
                    f in fields(data) if
                    getattr(data, f.name) is not None and
                    getattr(data, f.name) != []
                    ]
        shorten = self.__shorten_values_to_log(populated, 150)
        logger.debug(f"Module passed successfully. Data:\n    {'\n    '.join(shorten)}")