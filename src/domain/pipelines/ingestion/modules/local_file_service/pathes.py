from pathlib import Path


_THIS_FILE = Path(__file__).resolve()

ROOT = _THIS_FILE.parents[6]

RAW_DATA = ROOT / "src" / "domain" / "pipelines" / "ingestion" \
           / "modules" / "local_file_service" / "data_storage" / "raw_data"
PROCESSED_DATA = ROOT / "src" / "domain" / "pipelines" / "ingestion" \
           / "modules" / "local_file_service" / "data_storage" / "processed_data"