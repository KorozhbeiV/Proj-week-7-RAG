from pathlib import Path
from src.domain.pipelines.ingestion.complete.facades.abs_f_pre_processor import FilePreProcessor



class BaseFilePreProcessor(FilePreProcessor):
    def process_file(self, file: Path) -> str:
        """
        ## Simple reader method
        For more complex file processing implement it as a new class
        """
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
