import abc
from typing import Generic, TypeVar
from typing_extensions import Protocol


Element = TypeVar("Element", bound="ElementProtocol")


class ElementProtocol(Protocol):
    @property
    def uid(self) -> str:
        """Return Element's unique id"""


class Queue(abc.ABC, Generic[Element]):
    @abc.abstractmethod
    def get(self) -> Element:
        """Retrieve `Element` from queue"""

    @abc.abstractmethod
    def add(self, element: Element) -> None:
        """Add `Element` to queue"""

    @abc.abstractmethod
    def remove(self, uid: str) -> None:
        """Remove `Element` from queue based on uid"""

    @abc.abstractmethod
    def replace(self, uid: str, element: Element) -> None:
        """Replace `Element` based on uid"""
