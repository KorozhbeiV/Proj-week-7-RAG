from typing import Literal, Any, Unpack, overload
from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status
from src.domain.pipelines.ingestion.primitive.orcestration.abs_orchestrator import Orchestrator
from src.domain.pipelines.ingestion.primitive.orcestration.orchestrator import AddingOrchestrator, DeletingOrchestrator
from src.domain.pipelines.ingestion.primitive.orcestration.dict_type import AddedWkargs, DeletedKwargs


@overload
def get_orchestrator(action: Literal[Action.ADDED], status: Status, **kwargs: Unpack[AddedWkargs]) -> AddingOrchestrator:
    ...

@overload
def get_orchestrator(action: Literal[Action.DELETED], status: Status, **kwargs: Unpack[DeletedKwargs]) -> DeletingOrchestrator:
    ...

def get_orchestrator(action: Action, status: Status, **kwargs: Any) -> Orchestrator:
    return Orchestrator.registry[action.value](action, status, **kwargs)