import sys
from pathlib import Path
from src.domain.pipelines.ingestion.primitive import *
from src.domain.pipelines.ingestion.pipeline_entities.pathes import ROOT


sys.path.insert(0, str(ROOT))

orchestrator = PrimitiveOrchestrator(EmbedingClientCreatorKind.GEMINI_EMBEDING_CLIENT_CREATOR,
                                    ChunkingServiceKind.EMBEDING_CHUNKING_SERVICE,
                                    VectorDBServiceKind.QDRANT_DB_SERVICE, 
                                    ManifestManagerKind.SQLITE3,
                                    Status.SYNCED
                                    )

the_file = Path('/Users/getapple/Documents/Py_Projects/Proj week 7 RAG/dataset/raw_data/DnD5eSRD_md/DND5eSRD_001-018.md')


if __name__ == '__main__':
    orchestrator.process_file(the_file, Action.ADDED)