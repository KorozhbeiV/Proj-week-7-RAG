from enum import Enum



class Action(Enum):
    DELETED = 'deleted'
    ADDED = 'added'



class Status(Enum):
    PENDING = 'pending'
    FILE_PROCESSED = 'file_processed'
    CHUNKED = 'chunked'
    EMBEDED = 'embeded'
    VBD_UPDATED = 'vdb_updated'
    SYNCED = 'synced'
    METADATA_RETRIEVED = 'metadata_retrieved'



class FieldType(Enum):
    MAIN = 'main'
    FILE = 'metadata'
    CHUNK = 'internal'