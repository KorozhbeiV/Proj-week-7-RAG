from typing import Protocol, ClassVar, TypeVar, Self

TClass = TypeVar('TClass', bound="SupportRegistry")



class SupportRegistry(Protocol):
    registry: ClassVar[dict[str, type[Self]]]