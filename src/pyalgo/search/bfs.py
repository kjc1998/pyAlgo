import dataclasses
from pyalgo import models
from pyalgo.queue import priority
from typing import Dict, Generic, List, Optional


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
    def parent_uid(self) -> Optional[str]:
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


def breadth_first_search(map: models.ElementMap[models.Element]) -> models.SearchResult:
    """
    Perform a Breadth-First Search (DFS) on a given graph from start to end `Element`
    """

    @dataclasses.dataclass(frozen=True)
    class _SearchResult:
        solution: List[models.Element] = dataclasses.field(default_factory=list)
        searches: Dict[str, "_SearchTracker[models.Element]"] = dataclasses.field(
            default_factory=dict
        )

    visited = set([map.start])
    queue = priority.PriorityQueue([_SearchTracker([map.start], 0)])
    result = _SearchResult()

    def _check_end(search: "_SearchTracker[models.Element]") -> bool:
        """Check if search has reach end `Element`"""
        latest = search.elements[-1]
        return latest.uid == map.end.uid

    def _update_solution(search: "_SearchTracker[models.Element]") -> None:
        """Populate result with found solution"""
        for e in search.elements:
            result.solution.append(e)

    def _update_searches(search: "_SearchTracker[models.Element]") -> None:
        """Update search list in FIFO manner"""
        searches = result.searches
        if search.parent_uid and search.parent_uid in searches:
            del searches[search.parent_uid]
        searches[search.uid] = search

    def _update_queue(search: "_SearchTracker[models.Element]") -> None:
        """Add `Element` to priority queue based on search level"""
        elements = search.elements
        for e in map.get_next(elements[-1].uid):
            if e not in visited:
                new_ = _SearchTracker([*elements, e], search.level - 1)
                queue.add(new_)
                visited.add(e)

    while len(queue) > 0:
        search = queue.get()
        _update_searches(search)
        if _check_end(search):
            _update_solution(search)
            break
        _update_queue(search)

    return models.SearchResult(
        solution=result.solution,
        searches={i: s.elements for i, s in enumerate(result.searches.values())},
    )
