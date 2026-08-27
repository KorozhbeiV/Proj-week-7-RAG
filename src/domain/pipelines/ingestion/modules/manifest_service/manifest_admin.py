import sqlite3
from typing import Iterator
from contextlib import contextmanager
from pathlib import Path



class Sqlite3ManifestManager:
    def __init__(self, db: str | Path) -> None:
        self.db_path = Path(db)
        self.db_path.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    