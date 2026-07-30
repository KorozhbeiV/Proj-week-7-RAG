from typing import Literal, Any, overload

from google.genai import Client
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from api_keys import GEMINI_API_KEY



class ClientManager:
    def __init__(self,
                 model_name: Literal['gemini-3.1-flash-lite',
                                'gemini-embedding-2'
                                ]
                 ) -> None:
        self._model_name = model_name
    
    @staticmethod
    def _create_raw_client() -> Client:
        return Client(api_key=GEMINI_API_KEY)


    def ebmeding_client(self) -> GoogleGenerativeAIEmbeddings:
        """
        ## This method is dedicated only to use with embeding models 
        """
        return GoogleGenerativeAIEmbeddings(
            client=self._create_raw_client(),
            model=f'models/{self._model_name}'
        )

    def llm_client(self, config: dict[str, Any]) -> BaseChatModel:
        return ChatGoogleGenerativeAI(client=self._create_raw_client(), **config)

    @overload
    def create_llm_config(self, model_name: str | None, cache: str, sys_prompt: None) -> dict[str, Any]: ...
    
    @overload
    def create_llm_config(self, model_name: str | None, cache: None, sys_prompt: str) -> dict[str, Any]: ...


    def create_llm_config(self, model_name: str | None, cache: str | None, sys_prompt: str | None) -> dict[str, Any]:
        return {
            "model": model_name or self._model_name,
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
