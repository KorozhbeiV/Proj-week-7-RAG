from enum import Enum



class Action(Enum):
    DELETED = 'deleted'
    ADDED = 'added'
    UPDATED = 'updated'



class Status(Enum):
    PENDING = 'pending'
    VBD_UPDATED = 'vdb_updated'
    CHUNKED = 'chunked'
    EMBEDED = 'embeded'
    SYNCED = 'synced'
