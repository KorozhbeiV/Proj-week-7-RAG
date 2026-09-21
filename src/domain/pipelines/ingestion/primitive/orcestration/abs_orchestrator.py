from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar
from src.domain.pipelines.ingestion.protocols.primitive_support_registry import SupportRegistry

if TYPE_CHECKING:
    from pathlib import Path
    from enum import Enum
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.shared_abstracts.abs_ingestion_pipeline import IngestionPipeline
    from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status




class Orchestrator(ABC, SupportRegistry):
    registry: ClassVar[dict[str, type[Orchestrator]]] = {}

    def __init__(self,
                action: Action,
                status_to_stop: Status,
                **kwargs: Any
                ) -> None:
        """
        Use the fields of this class to store the Enum keys that are currently used\
            to extract concrete implementations of each module classes
        """
        self._action = action
        self._status_to_stop = status_to_stop
        self._module_keys = kwargs


    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            Orchestrator.registry[kind] = cls

    @staticmethod
    def _get_initial_context(file: Path, action: Action) -> IngestionPipelineContext:
        ...

    @staticmethod
    @abstractmethod
    def _logger(class_: type[object]) -> None:
        ...

    @abstractmethod
    def _create_executive_path(self, **kwargs: Any) -> dict[Enum, IngestionPipeline]:
        """
        Creates dictionary that pipeline uses to move through modules along a deterministic path
        """
        ...

    @abstractmethod
    def _execute_modules(self,
                        initial_context: IngestionPipelineContext,
                        executive_path: dict[Enum, IngestionPipeline]
                        ) -> None:
        """
        Iterate through different modules
        """
        ...

    @abstractmethod
    def process_file(self, file: Path) -> None:
        """
        Endpoin method
        """
        ...
