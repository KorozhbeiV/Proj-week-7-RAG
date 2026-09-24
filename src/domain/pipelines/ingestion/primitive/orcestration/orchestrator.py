from enum import Enum
from pathlib import Path
from dataclasses import fields
from typing import Unpack, Any
from src.shared.logger_config import logger
from src.domain.pipelines.ingestion.primitive.orcestration.abs_orchestrator import Orchestrator
from src.domain.pipelines.ingestion.pipeline_entities.enums import Status, Action
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.shared_abstracts.abs_ingestion_pipeline import IngestionPipeline
from src.domain.pipelines.ingestion.primitive.orcestration.dict_type import AddedWkargs, DeletedKwargs
from src.domain.pipelines.shared_modules.facades\
    import abs_chunking_service, abs_embeding_client, abs_vector_db_service, abs_manifest_service

ChunkingService = abs_chunking_service.ChunkingService
EmbedClientCreator = abs_embeding_client.EmbedClientCreator
VectorDBService = abs_vector_db_service.VectorDBService
ManifestManager = abs_manifest_service.ManifestManager



class BaseOrchestrator(Orchestrator):
    def __init__(self, action: Action, status_to_stop: Status, **kwargs: Any) -> None:
        super().__init__(action, status_to_stop, **kwargs)
    
    @staticmethod
    def _logger(class_: type[object]) -> None:
        logger.debug(f'Deffined: {class_}')

    @staticmethod
    def _get_initial_context(file: Path, action: Action) -> IngestionPipelineContext:
        return IngestionPipelineContext(file, action, status=Status.FILE_PROCESSED)


    def _execute_modules(self, initial_context: IngestionPipelineContext, executive_path: dict[Enum, IngestionPipeline]) -> None:
        while initial_context.status != self._status_to_stop:
            module = executive_path[initial_context.status]
            initial_context = module.execute_module(initial_context)


    def process_file(self, file: Path) -> None:
        context = self._get_initial_context(file, self._action)
        context_to_log = [getattr(context, f.name) for f in fields(context)]
        logger.info(f'Created initial context: {context_to_log}')

        logger.debug(f"Deffined path builder strategy: '{self._action.value}'")
        path = self._create_executive_path(**self._module_keys)
        path_to_log = [f"{k}: {type(v)}" for k, v in path.items()]
        logger.info(f"Executive path is created: {path_to_log}")

        self._execute_modules(context, path)



class AddingOrchestrator(BaseOrchestrator, kind=Action.ADDED.value):
    def _create_executive_path(self,
                            **kwargs: Unpack[AddedWkargs]
                            ) -> dict[Enum, IngestionPipeline]:
        Client = EmbedClientCreator.registry[kwargs['embeding_key'].value]
        embeding_client = Client(None)
        embed_model = embeding_client.create_ebmeding_client()
        self._logger(Client)

        Service = ChunkingService.registry[kwargs['chunking_service_key'].value]
        chunking_service = Service(embed_model)
        self._logger(Service)

        Db = VectorDBService.registry[kwargs['vdb_key'].value]
        vdb = Db.create(embed_model)
        self._logger(Db)

        Manifest = ManifestManager.registry[kwargs['manifest_key'].value]
        self._logger(Manifest)
        
        return {Status.FILE_PROCESSED: chunking_service, Status.CHUNKED: vdb, Status.VBD_UPDATED: Manifest()}



class DeletingOrchestrator(BaseOrchestrator, kind=Action.DELETED.value):
    def _create_executive_path(self,
                            **kwargs: Unpack[DeletedKwargs]
                            ) -> dict[Enum, IngestionPipeline]:
        Client = EmbedClientCreator.registry[kwargs['embeding_key'].value]
        embeding_client = Client(None)
        embed_model = embeding_client.create_ebmeding_client()
        self._logger(Client)

        Db = VectorDBService.registry[kwargs['vdb_key'].value]
        vdb = Db.create(embed_model)
        self._logger(Db)

        Manifest = ManifestManager.registry[kwargs['manifest_key'].value]
        self._logger(Manifest)
        manifest = Manifest()

        return {Status.FILE_PROCESSED: manifest, Status.METADATA_RETRIEVED: vdb, Status.VBD_UPDATED: manifest}