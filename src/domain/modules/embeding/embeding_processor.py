from typing import TYPE_CHECKING, overload

from langchain_core.embeddings import Embeddings

from src.domain.facades.abs_embeding_processor import EmbedingProcessor

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings



class BaseEmbedingProcessor(EmbedingProcessor):
    def __init__(self, embeding_model: Embeddings) -> None:
        super().__init__(embeding_model)

    @overload
    def to_embedings(self, text: str) -> list[float]: ...

    @overload
    def to_embedings(self, text: list[str]) -> list[list[float]]: ...
    
    def to_embedings(self, text: str | list[str]) -> list[float] | list[list[float]]:
        if isinstance(text, str):
            result = self.embeding_model.embed_query(text)
        else:
            result = self.embeding_model.embed_documents(text)
        return result