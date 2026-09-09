from typing import TYPE_CHECKING, Any
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext



class IngestionPipeline(ABC):
    """
    ## Main orchestrating class
    - Uses `execute_module` method to encapsulate concrete modules and\
        wrap their pipelines into a single method
    """
    def __init_subclass__(cls, **kwargs: Any) -> None:
        return super().__init_subclass__(**kwargs)
    

    @abstractmethod
    def execute_module(self,
                    data: IngestionPipelineContext
                    ) -> IngestionPipelineContext:
        """
        ## Hide each module's pipeline behid this method
        - Returns mutated object that recieves
        - Each module guarantees that it writes fields that only this module can work with
        """
        ...