from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

from pathlib import Path



class PrepareManager:
    @staticmethod
    def read_file(file: Path) -> str:
        with open(file, "r", encoding='utf-8') as f:
            return f.read()
        

    def split_on_chunks(self,
                        text: str,
                        embeding_model: GoogleGenerativeAIEmbeddings
                        ) -> list[str]:
        splitter = SemanticChunker(embeddings=embeding_model)
        return splitter.split_text(text)

    
        