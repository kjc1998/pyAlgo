import decimal
import dataclasses
from pyalgo import models
from pyalgo.queue import queue, priority
from pyalgo.search import linked_search
from typing import Any, Callable, Dict, List, Optional, Union

SearchTracker = linked_search.SearchTracker


class _BFSSearchTracker(SearchTracker[models.Element]):
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


def queue_search(
    map: models.ElementMap[models.Element],
    queue: queue.Queue[Any],
    convert: Callable[[List[models.Element]], SearchTracker[models.Element]],
) -> models.SearchResult:
    """
    Generic method for traversing through mapped `Element`s
    Input:
        map     : Mapper object linking `Element`s
        queue   : `Queue` object (NOTE: queue instance should be responsible of managing given objects, i.e.
                  raise an Error if objects handled do not conform to a set Signature type)
        convert : Callable that converts `Element` to `LinkSearch` type (for tracking `Element`s traversed)
    Output:
        SearchResult
    """

    @dataclasses.dataclass(frozen=True)
    class _SearchResult:
        solution: List[models.ElementProtocol] = dataclasses.field(default_factory=list)
        searches: Dict[str, SearchTracker[models.Element]] = dataclasses.field(
            default_factory=dict
        )

    queue.add(convert([map.start]))
    result = _SearchResult()

    def _check_visited(search: SearchTracker[models.Element]) -> bool:
        """Check if current tracker has already visited latest `Element`"""
        latest = search.elements[-1]
        return latest in search.elements[:-1]

    def _check_end(search: SearchTracker[models.Element]) -> bool:
        """Check if search has reach end `Element`"""
        latest = search.elements[-1]
        return latest.uid == map.end.uid

    def _update_searches(search: SearchTracker[models.Element]) -> None:
        """Update search list in FIFO manner"""
        searches = result.searches
        if search.previous_uid and search.previous_uid in searches:
            del searches[search.previous_uid]
        searches[search.uid] = search

    def _update_solution(search: SearchTracker[models.Element]) -> None:
        """Populate result with found solution"""
        for e in search.elements:
            result.solution.append(e)

    def _update_queue(search: SearchTracker[models.Element]) -> None:
        """Add `Element` to Queue"""
        elements = search.elements
        for e in map.get_next(elements[-1].uid):
            converted = convert([*search.elements, e])
            queue.add(converted)

    while len(queue) > 0:
        search = queue.get()
        if not _check_visited(search):
            _update_searches(search)
            if _check_end(search):
                _update_solution(search)
                break
            _update_queue(search)

    return models.SearchResult(
        solution=result.solution,
        searches={i: s.elements for i, s in enumerate(result.searches.values())},
    )


def breadth_first_search(map: models.ElementMap[models.Element]) -> models.SearchResult:
    """
    Perform a Breadth-First Search (DFS) on a given graph from start to end `Element`
    """

    def _convert(elements: List[models.Element]) -> _BFSSearchTracker[models.Element]:
        # NOTE: Adjusting weight can achieve different search patterns
        # i.e. for depth-first-search, set the weight to match proportionally with number of elements, ensuring newer elements to be at front
        # in breadth-first-search, set the weight based on levels in reversed order
        return _BFSSearchTracker(elements)

    queue = priority.PriorityQueue[_BFSSearchTracker[models.Element]]()
    return queue_search(map, queue, _convert)
