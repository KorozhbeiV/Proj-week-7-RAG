from typing import ClassVar, Any, Literal, TYPE_CHECKING
from abc import abstractmethod
from src.domain.pipelines.ingestion.primitive.facades.abs_main_pipeline_class import IngestionPipeline

if TYPE_CHECKING:
    from pathlib import Path
    from src.domain.pipelines.ingestion.complete.facades.abs_f_pre_processor import FilePreProcessor
    from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
    from src.domain.pipelines.ingestion.pipeline_entities.enums import Action
    from src.domain.pipelines.ingestion.complete.facades.abs_hashing_service import HashingService



class FileAdministrator(IngestionPipeline):
    registry: ClassVar[dict[str, type[FileAdministrator]]]

    def __init__(self, pre_processor: type[FilePreProcessor], hasher: type[HashingService]) -> None:
        self._pre_processor = pre_processor()
        self._hasher = hasher()
        self._recent_file_metadata: IngestionPipelineContext


    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            FileAdministrator.registry[kind] = cls
    
    @abstractmethod
    def _add_metadata(self, file_path: Path, action: Action, hash_: str) -> None:
        ...
    
    @abstractmethod
    def _extract_element_names(self, dir: Path, iter_mode: Literal['file', 'folder']) -> set[str]:
        ...
    
    @abstractmethod
    def _find_unmatched_files(self) -> tuple[set[str], set[str]]:
        ...
    
    @abstractmethod
    def _define_main_dir(self, folder: Path, file_name: str) -> Path:
        ...
    
    @abstractmethod
    def _create_sub_dirs(self, main_path: Path) -> None:
        ...

    @abstractmethod
    def _save_file_to_main_dir(self, file: str,
                                folder_path: Path,
                                folder_name: str
                                ) -> None:
        ...
    
    @abstractmethod
    def find_raw_data_left(self) -> list[str]:
        ...
    
    @abstractmethod
    def find_irrelevant_processed_data_left(self) -> list[str]:
        ...

    @abstractmethod
    def add_file(self, file_path: Path, update: bool = False) -> None:
        ...

    @abstractmethod
    def delete_file(self, file_name: str, delete_raw: bool = True) -> bool:
        ...

    @abstractmethod
    def return_metadata(self) -> IngestionPipelineContext:
        ...