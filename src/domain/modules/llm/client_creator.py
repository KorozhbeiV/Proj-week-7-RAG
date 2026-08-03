from typing import Any, overload, TypeVar

from google.genai import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from src.domain.shared.api_keys import GEMINI_API_KEY
from src.domain.facades.abs_llm_client import ClientCreator

TNativeClient = TypeVar('TNativeClient')



class BaseClientCreator(ClientCreator[TNativeClient]):
    ...



class GeminiClientCreator(BaseClientCreator[Client]):
    def __init__(self,
                 model_name: str | None
                 ) -> None:
        super().__init__(model_name or 'gemini-3.1-flash-lite')
    
    @staticmethod
    def _create_raw_client() -> Client:
        return Client(api_key=GEMINI_API_KEY)


    def llm_client(self, config: dict[str, Any]) -> BaseChatModel:
        return ChatGoogleGenerativeAI(client=self._create_raw_client(), **config)

    @overload
    def create_llm_config(self, cache: str, sys_prompt: None) -> dict[str, Any]: ...
    
    @overload
    def create_llm_config(self, cache: None, sys_prompt: str) -> dict[str, Any]: ...


    def create_llm_config(self, cache: str | None, sys_prompt: str | None) -> dict[str, Any]:
        return {
            "model": self._model_name,
            "temperature": 0.1,
            "max_output_tokens": 1024,
            "cached_content": cache,
            "seed": 42,
            "model_kwargs": {
                "presence_penalty": 0.5,
                "frequency_penalty": 0.4,
                "system_instruction": sys_prompt,
                }
            }
