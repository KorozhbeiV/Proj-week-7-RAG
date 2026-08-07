from enum import Enum



class AbstractClassType(Enum):
    CHUNKING_SERVICE = 'chunking_service'
    EMBEDING_CLIENT_CREATOR = 'embeding_client_creator'
    LLM_CLIENT_CREATOR = 'llm_client_creator'
    VECTOR_DB_SERVICE = 'vector_db_service'



class ChunkingServiceKind(Enum):
    EMBEDING_CHUNKING_SERVICE = 'embeding_chunking_service'



class EmbedingClientCreatorKind(Enum):
    GEMINI_EMBEDING_CLIENT_CREATOR = 'gemini_embeding_client_creator'



class LlmClientCreatorKind(Enum):
    GEMINI_CLIENT_CREATOR = 'gemini_client_creator'



class VectorDBServiceKind(Enum):
    QDRANT_DB_SERVICE = 'qdrant_db_service'