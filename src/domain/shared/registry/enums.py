from enum import Enum



class ChunkingServiceKind(Enum):
    EMBEDING_CHUNKING_SERVICE = 'embeding_chunking_service'



class EmbedingClientCreatorKind(Enum):
    GEMINI_EMBEDING_CLIENT_CREATOR = 'gemini_embeding_client_creator'



class LlmClientCreatorKind(Enum):
    GEMINI_LLM_CLIENT_CREATOR = 'gemini_llm_client_creator'



class VectorDBServiceKind(Enum):
    QDRANT_DB_SERVICE = 'qdrant_db_service'



class FileAdministratorKInd(Enum):
    ... # No concrete implementations yet