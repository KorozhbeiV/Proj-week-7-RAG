from __future__ import annotations
from typing import Any
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from src.domain.pipelines.ingestion.pipeline_entities.enums import Action, Status



@dataclass
class IngestionPipelineContext:
    # file_administrator module
    f_path: Path | None = None
    action: Action | None = None
    file_hash: str | None = None
    timestamp: datetime | None = None
    # chunking module
    chunks: list[str] | None = None
    chunk_count: int | None = None
    chinking_type: str | None = None
    # embeding_client module
    embeding_client: Any | None = None
    embeding_model: str | None = None
    # vector_db_service module
    chunks_id_added: list[int | str] = []
    chunks_id_updated: list[int | str] = []
    deleted_success: bool | None = None
    # manifest module
    full_metadata: list[dict[str, Any]] = []
    # global status, main pipeline parameter
    status: Status = Status.PENDING
