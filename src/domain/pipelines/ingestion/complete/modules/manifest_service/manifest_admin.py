import sqlite3
import json
import dataclasses
from typing import Iterator, Any
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from datetime import datetime
from domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.complete.facades.abs_manifest_service import ManifestManager
from src.domain.pipelines.ingestion.pipeline_entities.enums import Status, FieldType



class BaseManifestManager(ManifestManager):
    def __init__(self, db: str | Path | None = None) -> None:
        super().__init__(db)


    def _json_serializer(self, obj: object) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Cannot serialize {type[obj]}")
    

    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        self.init_database()
        result = self.load_data(data)
        assert result == True
        return data



class Sqlite3ManifestManager(BaseManifestManager):
    @contextmanager
    def __connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
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


    def load_data(self, data: IngestionPipelineContext) -> bool:
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
    def __metadata_filter(field: dataclasses.Field[IngestionPipelineContext],
                        file_type: FieldType
                        ) -> bool:
        return field.metadata.get('type') == file_type


    def _update_metadata(self, data: IngestionPipelineContext) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        file_data = {
                f.name: getattr(data, f.name) for
                f in dataclasses.fields(data) if
                self.__metadata_filter(f, FieldType.FILE)
            }
        assert (t_chunks := data.text_chunk) is not None
        assert (chunk_num := len(t_chunks)) == (id_num := len(data.chunk_ids)),\
            (f"Expected even number of chunks and ids. Given chunks: {chunk_num}, ids: {id_num}")
        
        chunk_data: list[dict[str, Any]] = [{"text_chunk": chunk, "chunk_ids": ids}
                      for chunk, ids in zip(t_chunks, data.chunk_ids)]
        return {"file": file_data, "chunks": chunk_data}
    

    