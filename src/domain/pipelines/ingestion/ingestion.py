import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from src.domain.pipelines.ingestion.primitive import *



orchestrator = get_orchestrator(Action.DELETED,
                                Status.SYNCED,
                                manifest_key=ManifestManagerKind.SQLITE3,
                                vdb_key=VectorDBServiceKind.QDRANT_DB_SERVICE,
                                embeding_key=EmbedingClientCreatorKind.GEMINI_EMBEDING_CLIENT_CREATOR,
                                # chunking_service_key=ChunkingServiceKind.EMBEDING_CHUNKING_SERVICE
                                )


the_file = Path('/Users/getapple/Documents/Py_Projects/Proj week 7 RAG/dataset/raw_data/DnD5eSRD_md/DND5eSRD_077-086.md')

if __name__ == '__main__':
    orchestrator.process_file(the_file)