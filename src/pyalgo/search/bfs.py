import dataclasses
from pyalgo import models
from pyalgo.queue import queue, priority
from typing import Any, Callable, Dict, Generic, List, Optional, Set

LinkSearchT = models.LinkSearchProtocol


class _SearchTracker(Generic[models.Element]):
    """
    Wrapper class to match signature of `PriorityQueue`, on top of additional properties for tracking `Element`s traversed
    """

    def __init__(self, elements: List[models.Element], level: int):
        self._elements = elements
        self._level = level
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
    def level(self) -> int:
        return self._level

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._elements == other._elements and self._level == other._level
        return False

    def __hash__(self) -> int:
        return hash(self)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._level < other._level
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._level < +other._level
        return False

    def __mt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._level > other._level
        return False

    def __me__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._level >= other._level
        return False

    def _post_init(self) -> None:
        if len(self._elements) == 0:
            raise ValueError(
                "can't instantiate search tracker with empty list of `Element`s"
            )


def queue_search(
    map: models.ElementMap[models.Element],
    queue: queue.Queue[Any],
    convert: Callable[
        [models.Element, Optional[LinkSearchT[models.Element]]],
        LinkSearchT[models.Element],
    ],
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
        searches: Dict[str, LinkSearchT[models.Element]] = dataclasses.field(
            default_factory=dict
        )

    queue.add(convert(map.start, None))
    visited: Set[models.Element] = set()
    result = _SearchResult()

    def _check_visited(search: LinkSearchT[models.Element]) -> bool:
        """Check if current element has been visited"""
        latest = search.elements[-1]
        return latest in visited

    def _check_end(search: LinkSearchT[models.Element]) -> bool:
        """Check if search has reach end `Element`"""
        latest = search.elements[-1]
        return latest.uid == map.end.uid

    def _update_visited(search: LinkSearchT[models.Element]) -> None:
        """Update visited Elements"""
        latest = search.elements[-1]
        visited.add(latest)

    def _update_searches(search: LinkSearchT[models.Element]) -> None:
        """Update search list in FIFO manner"""
        searches = result.searches
        if search.previous_uid and search.previous_uid in searches:
            del searches[search.previous_uid]
        searches[search.uid] = search

    def _update_solution(search: LinkSearchT[models.Element]) -> None:
        """Populate result with found solution"""
        for e in search.elements:
            result.solution.append(e)

    def _update_queue(search: LinkSearchT[models.Element]) -> None:
        """Add `Element` to Queue"""
        elements = search.elements
        for e in map.get_next(elements[-1].uid):
            if e not in visited:
                converted = convert(e, search)
                queue.add(converted)

    while len(queue) > 0:
        search = queue.get()
        if not _check_visited(search):
            _update_visited(search)
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

    def _convert(
        element: models.Element, previous_search: Optional[LinkSearchT[models.Element]]
    ) -> LinkSearchT[models.Element]:
        if previous_search is None:
            return _SearchTracker([element], 0)
        elif isinstance(previous_search, _SearchTracker):
            elements = previous_search.elements
            return _SearchTracker([*elements, element], previous_search.level - 1)
        raise NotImplementedError

    queue = priority.PriorityQueue[_SearchTracker[models.Element]]()
    return queue_search(map, queue, _convert)
