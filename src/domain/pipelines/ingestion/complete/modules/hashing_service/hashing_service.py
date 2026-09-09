import hashlib
from pathlib import Path
from typing import overload
from src.domain.pipelines.ingestion.\
    complete.facades.abs_hashing_service import HashingService



class BaseHashingService(HashingService):
    @overload
    @staticmethod
    def hash_it(text: Path) -> str:
        ...
    
    @overload
    @staticmethod
    def hash_it(text: list[str]) -> list[str]:
        ...

    @staticmethod
    def hash_it(text: Path | list[str]) -> str | list[str]:
        if isinstance(text, Path):
            with open(text, 'rb') as f:
                return hashlib.file_digest(f, hashlib.sha256).hexdigest()
        else:
            return [
                hashlib.sha256(el.encode('utf-8')).hexdigest()
                for el in text]
            