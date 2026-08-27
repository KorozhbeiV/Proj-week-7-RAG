import shutil
import hashlib
from pathlib import Path
from typing import Literal, Callable
from datetime import datetime, timezone
from src.domain.pipelines.ingestion.facades.abs_f_pre_processor import FilePreProcessor
from src.domain.pipelines.ingestion.modules.local_file_service.pathes import RAW_DATA, PROCESSED_DATA
from src.domain.pipelines.ingestion.facades.abs_f_administrator import FileAdministrator
from src.domain.pipelines.ingestion.modules.local_file_service.config import CHUNKS_FOLDER_NAME, DEFAULT_FILE_NAME
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status



class BaseFileAdministrator(FileAdministrator):
    def __init__(self, pre_processor: type[FilePreProcessor]) -> None:
        super().__init__(pre_processor)
        self._recent_file_metadata: IngestionPipelineContext

    
    def _add_metadata(self, file_path: Path, action: Action, hash_: str) -> None:
        self._recent_file_metadata = IngestionPipelineContext(
            f_path=file_path, 
            action=action,
            timestamp=datetime.now(tz=timezone.utc),
            file_hash=hash_,
            status=Status.FILE_PROCESSED
            )
    

    def _extract_element_names(self, dir: Path, iter_mode: Literal['file', 'folder']) -> set[str]:
        file_func: Callable[[Path], bool] = lambda f: f.is_file()
        folder_func: Callable[[Path], bool] = lambda f: f.is_dir()
        registry: dict[str, Callable[[Path], bool]] = {"file": file_func, "folder": folder_func}
        is_valid = registry[iter_mode] # Whether the element is file or directory
        return {f.stem for f in dir.iterdir() if is_valid(f) and not f.stem.startswith('.')}
    

    def _find_unmatched_files(self) -> tuple[set[str], set[str]]:
        raw = self._extract_element_names(RAW_DATA, iter_mode='file')
        processed = self._extract_element_names(PROCESSED_DATA, iter_mode='folder')
        return raw, processed
    
    
    def _define_main_dir(self, folder: Path, file_name: str) -> Path:
        folder_path = next((f for
                            f in 
                            folder.iterdir() if 
                            f.is_dir() and 
                            f.stem == file_name), None)
        if folder_path is None:
            # Name of the folder = original file's name
            folder_path = (PROCESSED_DATA / file_name)
            folder_path.mkdir()
        return folder_path
    

    def _create_sub_dirs(self, main_path: Path) -> None:
        subloders: list[Path] = [main_path / CHUNKS_FOLDER_NAME, ]
        for el in subloders:
            if not el.exists():
                el.mkdir()

    
    def _save_file_to_main_dir(self, file: str,
                                folder_path: Path,
                                folder_name: str
                                ) -> None:
        file_path = folder_path / folder_name
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file)

    def _read_stream_hash(self, f_path: Path) -> str:
        with open(f_path, 'rb') as f:
            return hashlib.file_digest(f, hashlib.sha256).hexdigest()
    

    def find_raw_data_left(self) -> list[str]:
        raw, processed = self._find_unmatched_files()
        raw = raw - processed
        return list(raw)
    

    def find_irrelevant_processed_data_left(self) -> list[str]:
        raw, processed = self._find_unmatched_files()
        processed = processed - raw
        return list(processed)


    def add_file(self, file_path: Path, update: bool = False) -> None:
        processor = self._pre_processor
        processed = processor.process_file(file_path)

        folder_path = self._define_main_dir(PROCESSED_DATA, file_path.stem)
        self._create_sub_dirs(folder_path)

        content_exists = (folder_path / DEFAULT_FILE_NAME).exists()        
        if content_exists and not update:
            raise RuntimeError(f'File {file_path.stem} already processed and has the same hash.\
                               If you want to replace it- use `update = True` flag')
        
        action = Action.UPDATED if content_exists and update else Action.ADDED
        hash_ = self._read_stream_hash(file_path)
        self._add_metadata(file_path, action, hash_)
        # Default file name already contains an extension
        self._save_file_to_main_dir(processed, folder_path, DEFAULT_FILE_NAME)


    def delete_file(self, file_name: str, delete_raw: bool = True) -> bool:
        processed_folder = self._define_main_dir(PROCESSED_DATA, file_name)
        path_to_the_file = processed_folder / DEFAULT_FILE_NAME
        hash_ = self._read_stream_hash(path_to_the_file)

        if processed_folder.exists() and processed_folder.is_dir():
            shutil.rmtree(processed_folder)
        else:
            raise FileNotFoundError(f"File '{file_name}' was not\
                                    found within the given path: '{processed_folder}'")
        
        if delete_raw:
            raw_folder_path = RAW_DATA / file_name
            if (raw_file_exists := raw_folder_path.exists()) and processed_folder.is_file():
                shutil.rmtree(raw_folder_path)
            else:
                raise FileNotFoundError(f"File '{file_name}' was not\
                                        found within the given path: '{raw_folder_path}'")
        else:
            raw_file_exists = False
        self._add_metadata(processed_folder, Action.DELETED, hash_)

        if not processed_folder.exists() and not raw_file_exists:
            return True
        else:
            return False

    
    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        """
        No usage for `data` argument since this is the first module in line
        """
        return self._recent_file_metadata