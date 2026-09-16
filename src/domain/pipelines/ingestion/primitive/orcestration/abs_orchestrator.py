from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from enum import Enum
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.primitive.facades.abs_main_pipeline_class import IngestionPipeline
    from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status



class Orchestrator(ABC):
    def __init__(self, embeding_key: Enum,
                chunking_service_key: Enum, 
                vdb_key: Enum,
                manifest_key: Enum,
                status_to_stop: Status
                ) -> None:
        """
        Use the fields of this class to store the Enum keys that are currently used\
            to extract concrete implementations of each module classes
        """
        self._embeding_key = embeding_key
        self._chunking_service_key = chunking_service_key
        self._vdb_key = vdb_key
        self._manifest_key = manifest_key
        self._status_to_stop = status_to_stop

    @abstractmethod
    def process_file(self, file: Path, action: Action) -> None:
        """
        Endpoin method
        """
        ...

    @staticmethod
    @abstractmethod
    def _get_initial_context(file: Path, action: Action) -> IngestionPipelineContext:
        ...

    @abstractmethod
    def _create_executive_path(self) -> dict[str, IngestionPipeline]:
        """
        Creates dictionary that pipeline uses to move through modules along a deterministic path
        """
        ...

    @abstractmethod
    def _execute_modules(self,
                        initial_context: IngestionPipelineContext,
                        executive_path: dict[str, IngestionPipeline]
                        ) -> None:
        """
        Iterate through different modules
        """
        ...