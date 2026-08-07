from typing import TYPE_CHECKING, Generic, TypeVar, Any, ClassVar
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from langchain_core.language_models.chat_models import BaseChatModel

TNativeClient = TypeVar('TNativeClient')


class LlmClientCreator(ABC, Generic[TNativeClient]):
    register: ClassVar[dict[str, type[LlmClientCreator[Any]]]]

    def __init__(self,
                 model_name: str | None
                 ) -> None:
        self._model_name = model_name

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            LlmClientCreator.register[kind] = cls
    
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
