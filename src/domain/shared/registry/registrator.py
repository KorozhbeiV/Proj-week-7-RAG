from functools import wraps
from typing import TypeVar

TClass = TypeVar('TClass')


def registator(cls: TClass, ,) -> TClass: