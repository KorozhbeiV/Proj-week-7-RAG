"""
## An indoor module
- Is not called by executive pipeline
- Used as dependency injected module
"""

from pathlib import Path
from abc import ABC, abstractmethod



class FilePreProcessor(ABC):
    @abstractmethod
    def process_file(self, file: Path) -> str:
        ...