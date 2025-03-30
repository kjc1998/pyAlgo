import abc
from pyalgo.models import Element
from typing import Generic


class Tree(abc.ABC, Generic[Element]):
    """Tree Data Structure for organising `Element`"""

    @property
    @abc.abstractmethod
    def root(self) -> Element:
        raise NotImplementedError

    @abc.abstractmethod
    def insert(self, element: Element) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, uid: str) -> Element:
        raise NotImplementedError
