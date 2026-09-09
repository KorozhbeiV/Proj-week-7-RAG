from abc import ABC, abstractmethod
from pathlib import Path
from typing import overload



class HashingService(ABC):
    @overload
    @staticmethod
    def hash_it(text: Path) -> str:
        ...
    
    @overload
    @staticmethod
    def hash_it(text: list[str]) -> list[str]:
        ...
    
    @abstractmethod
    @staticmethod
    def hash_it(text: Path | list[str]) -> str | list[str]:
        ...