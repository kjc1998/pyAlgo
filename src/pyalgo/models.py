import abc
import decimal
from typing import Generic, List, TypeVar, Union
from typing_extensions import Protocol

Element = TypeVar("Element", bound="ElementProtocol")
WeightedElement = TypeVar("WeightedElement", bound="WeightedElementProtocol")


class ElementProtocol(Protocol):
    @property
    @abc.abstractmethod
    def uid(self) -> str:
        """Return Element's unique id"""

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check if `self` is equal to `other`"""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Element must be hashable"""


class WeightedElementProtocol(ElementProtocol, Protocol):
    """Similar to `ElementProtocol`, with comparison features"""

    @property
    @abc.abstractmethod
    def weight(self) -> Union[int, float, decimal.Decimal]:
        """Return weight of self"""


class ElementMap(abc.ABC, Generic[Element]):
    """Map and form relationship patterns between `Element`s"""

    @property
    @abc.abstractmethod
    def start(self) -> Element:
        """Return starting `Element`"""

    @property
    @abc.abstractmethod
    def end(self) -> Element:
        """Return ending `Element`"""

    @abc.abstractmethod
    def get_next(self, uid: str) -> List[Element]:
        """Return list of `Element`s given current uid"""
