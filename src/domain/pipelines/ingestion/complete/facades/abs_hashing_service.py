from abc import ABC, abstractmethod
from pathlib import Path
from typing import overload



class HashingService(ABC):
    @staticmethod
    @overload
    def hash_it(text: Path) -> str:
        ...
    
    @staticmethod
    @overload
    def hash_it(text: list[str]) -> list[str]:
        ...
    
    @staticmethod
    @abstractmethod
    def hash_it(text: Path | list[str]) -> str | list[str]:
        ...