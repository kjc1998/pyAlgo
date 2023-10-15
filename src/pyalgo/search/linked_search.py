import decimal
from pyalgo import models
from typing import List, Generic, Optional, Union
from typing_extensions import Protocol


class LinkedSearchProtocol(models.ElementProtocol, Protocol[models.Element]):
    """
    Search `Element`s Chaining
    (NOTE: Wrapper class on top of `Element`, nonetheless still an `Element` with `uid` and `hash` methods)
    Usage Example:
        Input: [1, 4, 7, 8]
        Create 4 unique `LinkSearch`s
            1) [1]
            2) [1, 4]
            3) [1, 4, 7]
            4) [1, 4, 7, 8]
    """

    @property
    def previous_uid(self) -> Optional[str]:
        """Return previous `LinkSearch` id"""

    @property
    def elements(self) -> List[models.Element]:
        """Return list of `Element`s"""


class _BasicSearchTracker(Generic[models.Element]):
    """
    Wrapper class to match signature of `PriorityQueue`, on top of additional properties for tracking `Element`s traversed
    NOTE: Subclass of both `LinkedSearchProtocol` and `WeightedElementProtocol`
    """

    def __init__(
        self, elements: List[models.Element], weight: Union[int, float, decimal.Decimal]
    ):
        self._elements = elements
        self._weight = weight
        self._post_init()

    @property
    def uid(self) -> str:
        uids = ",".join([e.uid for e in self._elements])
        return uids

    @property
    def previous_uid(self) -> Optional[str]:
        uids = ",".join([e.uid for e in self._elements[:-1]])
        return uids if uids else None

    @property
    def elements(self) -> List[models.Element]:
        return self._elements

    @property
    def weight(self) -> Union[int, float, decimal.Decimal]:
        return self._weight

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._elements == other._elements and self._weight == other._weight
        return False

    def __hash__(self) -> int:
        return hash(self)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._weight < other._weight
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._weight <= other._weight
        return False

    def __mt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._weight > other._weight
        return False

    def __me__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._weight >= other._weight
        return False

    def _post_init(self) -> None:
        if len(self._elements) == 0:
            raise ValueError(
                "can't instantiate search tracker with empty list of `Element`s"
            )


class _DijakstraPathTracker(_BasicSearchTracker[models.WeightedElement]):
    def __init__(self, elements: List[models.WeightedElement]):
        super().__init__(elements, sum([e.weight for e in elements]))
