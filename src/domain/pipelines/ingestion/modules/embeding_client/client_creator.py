from typing import TypeVar

from dataclasses import replace
from google.genai import Client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.shared.api_keys import GEMINI_API_KEY
from src.domain.pipelines.ingestion.facades.abs_embeding_client import EmbedClientCreator
from src.domain.shared.registry.enums import EmbedingClientCreatorKind

TNativeClient = TypeVar('TNativeClient')



class BaseEmbedClientCreator(EmbedClientCreator[TNativeClient]):
    def execute_module(self, data: IngestionPipelineContext) -> IngestionPipelineContext:
        return replace(data, embeding_model=self._model_name, embeding_client=self.create_ebmeding_client())



class GeminiEmbedClientCreator(BaseEmbedClientCreator[Client],
                               kind=EmbedingClientCreatorKind.GEMINI_EMBEDING_CLIENT_CREATOR.value
                               ):
    def __init__(self, model_name: str | None = None) -> None:
        super().__init__(model_name or 'gemini-embedding-2')

    @staticmethod
    def _create_raw_client() -> Client:
        return Client(api_key=GEMINI_API_KEY)


    def create_ebmeding_client(self) -> GoogleGenerativeAIEmbeddings:
        return GoogleGenerativeAIEmbeddings(
            client=self._create_raw_client(),
            model=f'models/{self._model_name}'
        )