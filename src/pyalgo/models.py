from typing import TypeVar
from typing_extensions import Protocol

Element = TypeVar("Element", bound="ElementProtocol")
WeightedElement = TypeVar("WeightedElement", bound="WeightedElementProtocol")


class ElementProtocol(Protocol):
    @property
    def uid(self) -> str:
        """Return Element's unique id"""

    def __hash__(self) -> int:
        """Element must be hashable"""


class WeightedElementProtocol(ElementProtocol, Protocol):
    """Similar to `ElementProtocol`, with comparison features"""

    def __eq__(self, other: object) -> bool:
        """Check if `self` is equal to `other`"""

    def __lt__(self, other: object) -> bool:
        """Check if `self` is less than `other`"""

    def __le__(self, other: object) -> bool:
        """Check if `self` is less than or equal to `other`"""

    def __mt__(self, other: object) -> bool:
        """Check if `self` weighs more than `other`"""

    def __me__(self, other: object) -> bool:
        """Check if `self` weighs more than or equal to `other`"""
