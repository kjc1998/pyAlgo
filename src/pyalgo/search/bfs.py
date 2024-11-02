import decimal
from pyalgo import models, queue as queue_
from pyalgo.search import queue_search
from typing import List, Optional, Union


class _BFSSearchTracker(queue_search.SearchTracker[models.Element]):
    """
    Wrapper class to match signature of `PriorityQueue`, on top of additional properties for tracking `Element`s traversed
    NOTE: Subclass of both `SearchTracker` and `WeightedElementProtocol`
    """

    def __init__(self, elements: List[models.Element]):
        self.__elements = elements
        self.__post_init()

    @property
    def uid(self) -> str:
        uids = ",".join([e.uid for e in self.__elements])
        return uids

    @property
    def previous_uid(self) -> Optional[str]:
        uids = ",".join([e.uid for e in self.__elements[:-1]])
        return uids if uids else None

    @property
    def elements(self) -> List[models.Element]:
        return self.__elements

    @property
    def weight(self) -> Union[int, float, decimal.Decimal]:
        """
        Weightage is dependent on number of elements stored.
        The greater the number, the lower its priority.
        """
        weight = -1 * len(self.__elements)
        return weight

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.__elements == other.__elements and self.weight == other.weight
        return False

    def __hash__(self) -> int:
        return hash(self)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight < other.weight
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight <= other.weight
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight > other.weight
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight >= other.weight
        return False

    def __post_init(self) -> None:
        if len(self.__elements) == 0:
            raise ValueError(
                "can't instantiate search tracker with empty list of `Element`s"
            )


def breadth_first_search(
    map: models.ElementMap[models.Element],
) -> queue_search.SearchResult:
    """
    Perform a Breadth-First Search (DFS) on a given graph from start to end `Element`
    """

    def _convert(elements: List[models.Element]) -> _BFSSearchTracker[models.Element]:
        # NOTE: Adjusting weight can achieve different search patterns
        # i.e. for depth-first-search, set the weight to match proportionally with number of elements, ensuring newer elements to be at front
        # in breadth-first-search, set the weight based on levels in reversed order
        return _BFSSearchTracker(elements)

    queue = queue_.PriorityQueue[_BFSSearchTracker[models.Element]]()
    return queue_search.queue_search(map, queue, _convert)
