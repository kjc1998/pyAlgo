import abc
import dataclasses
from typing import Dict, Generic, Iterable, List, TypeVar
from typing_extensions import Protocol

Element = TypeVar("Element", bound="ElementProtocol")
WeightedElement = TypeVar("WeightedElement", bound="WeightedElementProtocol")


class ElementProtocol(Protocol):
    @property
    def uid(self) -> str:
        """Return Element's unique id"""

    def __eq__(self, other: object) -> bool:
        """Check if `self` is equal to `other`"""

    def __hash__(self) -> int:
        """Element must be hashable"""


class WeightedElementProtocol(ElementProtocol, Protocol):
    """Similar to `ElementProtocol`, with comparison features"""

    def __lt__(self, other: object) -> bool:
        """Check if `self` is less than `other`"""

    def __le__(self, other: object) -> bool:
        """Check if `self` is less than or equal to `other`"""

    def __mt__(self, other: object) -> bool:
        """Check if `self` weighs more than `other`"""

    def __me__(self, other: object) -> bool:
        """Check if `self` weighs more than or equal to `other`"""


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


@dataclasses.dataclass
class SearchResult:
    """
    Search Result Model
    solution:   List of `Element`s from start to end
    searches:   Dict of searches done in order from 0 to n-1
    """

    solution: Iterable[ElementProtocol] = dataclasses.field(default_factory=list)
    searches: Dict[int, Iterable[ElementProtocol]] = dataclasses.field(
        default_factory=dict
    )
