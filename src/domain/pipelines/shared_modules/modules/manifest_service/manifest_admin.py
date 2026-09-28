import json
import sqlite3
from dataclasses import replace, Field, fields
from typing import Iterator, Any, cast
from enum import Enum
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from src.shared.logger_config import logger
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.shared_modules.facades.abs_manifest_service import ManifestManager
from src.domain.pipelines.ingestion.pipeline_entities.enums import Status, FieldType, Action, FileExists
from src.domain.pipelines.ingestion.pipeline_entities.registry_enums import ManifestManagerKind



class BaseManifestManager(ManifestManager):
    def __init__(self, db: str | Path | None = None) -> None:
        super().__init__(db)


    def _json_serializer(self, obj: object) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Cannot serialize {type[obj]}")
    
    
    def __adding_path(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        self.init_database()
        assert (result := self.load_new_data(data))
        result = replace(data, status=Status.SYNCED)
        self._log_changes(result)
        return result
    

    def __retrieve_metadata(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        self.init_database()
        metadata = self.retrieve_metadata(data)
        assert metadata is not None, "It's not allowed to retrieve empty metadata on existing record"
        result = replace(data, file_metadata=metadata, status=Status.METADATA_RETRIEVED)
        self._log_changes(result)
        return result
    

    def __delete_record(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        assert (path := data.f_path) is not None
        deleted = self.delete_record(path)
        assert deleted, f"The procces of delete was not proccesed successfully over the '{path}' file"
        return replace(data, status=Status.SYNCED)
    
    @staticmethod
    def __log_file_exists(f_path: Path | None, action: Action | None, exists: bool, continue_: bool) -> None:
        assert f_path is not None
        assert action is not None
        if exists:
            exists_msg = "exists"
        else:
            exists_msg = "not exists"
        if continue_:
            processing_action_msg = "Continue processing..."
        else:
            processing_action_msg = "Stoppping the pipeline."
        logger.debug(f"File {f_path.stem}. Action: {action} is {exists_msg}. {processing_action_msg}")


    def __check_file_exists(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        result = self.retrieve_metadata(data)
        if data.action == Action.ADDED:
            if result:
                exists = True
                continue_ = False
                to_replace = {"f_exists_check": FileExists.CONFIRMED, "status": Status.SYNCED}
            else:
                exists = False
                continue_ = True
                to_replace = {"f_exists_check": FileExists.NOT, "status": Status.MANIFEST_CONFIRMED}
        else:
            if result:
                exists = True
                continue_ = True
                to_replace = {"f_exists_check": FileExists.CONFIRMED, "status": Status.MANIFEST_CONFIRMED}
            else:
                exists = False
                continue_ = False
                to_replace: dict[str, Any] = {"f_exists_check": FileExists.NOT, "status": Status.SYNCED}
        self.__log_file_exists(data.f_path, data.action, exists, continue_)
        return replace(data, **to_replace)


    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        if data.f_exists_check == FileExists.REQUIRE_CHECK:
            return self.__check_file_exists(data)
        if data.delete_record_for_file:
            return self.__delete_record(data)
        if data.action == Action.ADDED:
            return self.__adding_path(data)
        if data.action == Action.DELETED:
            return self.__retrieve_metadata(data)
        raise RuntimeError(f"Unknown action '{data.action}' to perform in '{__file__}'")



class Sqlite3ManifestManager(BaseManifestManager, kind=ManifestManagerKind.SQLITE3.value):
    @contextmanager
    def __connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    
    def init_database(self) -> None:
        allowed = ", ".join(f"'{s.value}'" for s in Status)
        with self.__connection() as conn:
            conn.execute(f"""
                            CREATE TABLE IF NOT EXISTS manifest(
                                f_path TEXT PRIMARY KEY NOT NULL,
                                status TEXT NOT NULL CHECK(status IN ({allowed})),
                                metadata TEXT NOT NULL
                                )    
                        """)


    def load_new_data(self, data: IngestionPipelineContext) -> bool:
        with self.__connection() as conn:
            try:
                conn.execute("INSERT INTO manifest VALUES(?, ?, ?)",
                                (str(data.f_path),
                                data.status.value,
                                json.dumps(
                                    self._update_metadata(data),
                                    default=self._json_serializer
                                    )
                                )
                            )
                return True
            except:
                return False

    @staticmethod
    def __json_metadata_to_py(metadata_row: str) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        real_metadata = cast(dict[str, Any], json.loads(metadata_row))
        return real_metadata


    def retrieve_metadata(self, data: IngestionPipelineContext) -> dict[str, dict[str, Any] | list[dict[str, Any]]] | None:
        assert (f_path := data.f_path) is not None
        with self.__connection() as conn:
            result = conn.execute("SELECT metadata FROM manifest WHERE f_path = ?",
                        (str(f_path),))
            json_row = cast(sqlite3.Row | None, result.fetchone())
            if json_row is None:
                logger.debug(f"There's no data behind the '{f_path}' file withing manifest.")
                return json_row
            logger.debug(f"The data for '{f_path}' exists in manifest")
            return self.__json_metadata_to_py(json_row['metadata'])


    def delete_record(self, f_path: Path) -> bool:
        with self.__connection() as conn:
            try:
                conn.execute("DELETE FROM manifest WHERE f_path = ?",
                            (str(f_path),))
                return True
            except:
                return False

    @staticmethod
    def __metadata_filter(field: Field[IngestionPipelineContext],
                        file_type: FieldType
                        ) -> bool:
        return field.metadata.get('type') == file_type


    def _update_metadata(self, data: IngestionPipelineContext) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        file_data = {f.name: getattr(data, f.name) for
                    f in fields(data) if
                    self.__metadata_filter(f, FieldType.FILE)
                    }
        assert (t_chunks := data.text_chunk) is not None
        assert (chunk_num := len(t_chunks)) == (id_num := len(data.chunk_ids)),\
            (f"Expected even number of chunks and ids. Given chunks: {chunk_num}, ids: {id_num}")
        
        chunk_data: list[dict[str, Any]] = [{"text_chunk": chunk, "chunk_ids": ids}
                      for chunk, ids in zip(t_chunks, data.chunk_ids)]
        return {"file": file_data, "chunks": chunk_data}
    

    