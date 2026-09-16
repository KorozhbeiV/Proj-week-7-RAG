from enum import Enum
from pathlib import Path
from src.domain.pipelines.ingestion.primitive.orcestration.abs_orchestrator import Orchestrator
from src.domain.pipelines.ingestion.pipeline_entities.enums import Status, Action
from src.domain.pipelines.ingestion.pipeline_entities.data_classes import IngestionPipelineContext
from src.domain.pipelines.ingestion.primitive.facades\
    import abs_chunking_service, abs_embeding_client, abs_vector_db_service, abs_main_pipeline_class
from src.domain.pipelines.ingestion.complete.facades.abs_manifest_service import ManifestManager

IngestionPipeline = abs_main_pipeline_class.IngestionPipeline
ChunkingService = abs_chunking_service.ChunkingService
EmbedClientCreator = abs_embeding_client.EmbedClientCreator
VectorDBService = abs_vector_db_service.VectorDBService



class PrimitiveOrchestrator(Orchestrator):
    def __init__(self, embeding_key: Enum,
                chunking_service_key: Enum, 
                vdb_key: Enum,
                manifest_key: Enum,
                status_to_stop: Status
                ) -> None:
        super().__init__(embeding_key, chunking_service_key, vdb_key, manifest_key, status_to_stop)


    @staticmethod
    def _get_initial_context(file: Path, action: Action) -> IngestionPipelineContext:
        return IngestionPipelineContext(file, action, status=Status.FILE_PROCESSED)


    def _create_executive_path(self) -> dict[str, IngestionPipeline]:
        Client = EmbedClientCreator.registry[self._embeding_key.value]
        embeding_client = Client(None)
        embed_model = embeding_client.create_ebmeding_client()

        Service = ChunkingService.registry[self._chunking_service_key.value]
        chunking_service = Service(embed_model)

        Db = VectorDBService.registry[self._vdb_key.value]
        vdb = Db.create(embed_model)

        manifest = ManifestManager.registry[self._manifest_key.value]()
        
        return {Status.FILE_PROCESSED.value: chunking_service, Status.CHUNKED.value: vdb, Status.VBD_UPDATED.value: manifest}
    

    def _execute_modules(self, initial_context: IngestionPipelineContext, executive_path: dict[str, IngestionPipeline]) -> None:
        while initial_context.status != self._status_to_stop:
            module = executive_path[initial_context.status.value]
            result = module.execute_module(initial_context)
            print(result)
    

    def process_file(self, file: Path, action: Action) -> None:
        context = self._get_initial_context(file, action)
        path = self._create_executive_path()
        self._execute_modules(context, path)