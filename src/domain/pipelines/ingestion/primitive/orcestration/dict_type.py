from typing import TypedDict, Any, NotRequired
from enum import Enum


class _SharedKwargs(TypedDict):
    vdb_key: Enum
    manifest_key: Enum
    embeding_key: Enum
    other: NotRequired[Any]


class AddedWkargs(_SharedKwargs):
    chunking_service_key: Enum



class DeletedKwargs(_SharedKwargs):
    ...