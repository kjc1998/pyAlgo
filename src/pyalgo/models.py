from typing import TypeVar
from typing_extensions import Protocol

Element = TypeVar("Element", bound="ElementProtocol")


class ElementProtocol(Protocol):
    @property
    def uid(self) -> str:
        """Return Element's unique id"""
