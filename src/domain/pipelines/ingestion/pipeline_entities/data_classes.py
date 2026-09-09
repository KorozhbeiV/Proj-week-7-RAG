from typing import Any
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from src.domain.pipelines.ingestion.\
    pipeline_entities.enums import Action, Status, FieldType



@dataclass
class IngestionPipelineContext:
    # file_administrator module
    f_path: Path | None = field(
        default=None,
        metadata={'type': FieldType.MAIN, 'chunk_metadata': True}
        )
    action: Action | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': False}
        )
    file_hash: str | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': True}
        )
    timestamp: datetime | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': False}
        )
    # chunking module
    text_chunk: list[str] | None = field(
        default=None,
        metadata={'type': FieldType.CHUNK, 'chunk_metadata': False}
        )
    chunk_count: int | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': True}
        )
    chinking_type: str | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': False}
        )
    # embeding_client module
    embeding_client: Any | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': False}
        )
    embeding_model: str | None = field(
        default=None,
        metadata={'type': FieldType.FILE, 'chunk_metadata': False}
        )
    # vector_db_service module
    chunk_ids: list[int | str] = field(
        default_factory=list[int | str],
        metadata={'type': FieldType.CHUNK, 'chunk_metadata': False}
        )
    chunks_deleted: bool | None = None
    # manifest module
    chunk_metadata: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]])
    # global status, main pipeline parameter
    status: Status = field(
        default=Status.PENDING,
        metadata={'type': FieldType.MAIN, 'chunk_metadata': False}
        )