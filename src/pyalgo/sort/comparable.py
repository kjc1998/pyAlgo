import abc
from typing import Any, Hashable, TypeVar
from typing_extensions import Protocol


Comparable = TypeVar("Comparable", bound="ComparableElementProtocol")


class ComparableElementProtocol(Hashable, Protocol):
    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Check if `self` equals to `other`"""

    @abc.abstractmethod
    def __ne__(self, other: Any) -> bool:
        """Check if `self` is not equal to `other`"""

    @abc.abstractmethod
    def __lt__(self, other: Any) -> bool:
        """Check if `self` is less than `other`"""

    @abc.abstractmethod
    def __le__(self, other: Any) -> bool:
        """Check if `self` is less or equal than `other`"""

    @abc.abstractmethod
    def __gt__(self, other: Any) -> bool:
        """Check if `self` is greater than `other`"""

    @abc.abstractmethod
    def __ge__(self, other: Any) -> bool:
        """Check if `self` is greater or equal to `other`"""
