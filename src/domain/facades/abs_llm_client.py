from typing import TYPE_CHECKING, Generic, TypeVar, Any
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.language_models.chat_models import BaseChatModel

TNativeClient = TypeVar('TNativeClient')


class ClientCreator(ABC, Generic[TNativeClient]):
    def __init__(self,
                 model_name: str | None
                 ) -> None:
        self._model_name = model_name
    
    @staticmethod
    @abstractmethod
    def _create_raw_client() -> TNativeClient:
        ...

    @abstractmethod
    def llm_client(self, config: dict[str, Any]) -> BaseChatModel:
        ...

    @abstractmethod
    def create_llm_config(self, cache: str | None, sys_prompt: str | None) -> dict[str, Any]:
        ...
