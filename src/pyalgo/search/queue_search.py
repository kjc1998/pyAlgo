import abc
import dataclasses
from pyalgo import models
from pyalgo.queue import queue
from typing import Any, Callable, Dict, Iterable, List, Optional, Generic


@dataclasses.dataclass
class SearchResult:
    """
    Search Result Model
    solution:   List of `Element`s from start to end
    searches:   Dict of searches done in order from 0 to n-1
    """

    solution: Iterable[models.ElementProtocol] = dataclasses.field(default_factory=list)
    searches: Dict[int, Iterable[models.ElementProtocol]] = dataclasses.field(
        default_factory=dict
    )


class SearchTracker(abc.ABC, Generic[models.Element]):
    """
    Search `Element`s Chaining
    (NOTE: Wrapper class on top of `Element`, nonetheless still an `Element` with `uid` and `hash` methods)
    Example:
        Input: [1, 4, 7, 8]
        List consists of 4 unique `LinkSearch`s
            1) [1]
            2) [1, 4]
            3) [1, 4, 7]
            4) [1, 4, 7, 8]
    """

    @property
    @abc.abstractmethod
    def uid(self) -> str:
        """Return Element's unique id"""

    @property
    @abc.abstractmethod
    def previous_uid(self) -> Optional[str]:
        """Return previous `LinkSearch` id"""

    @property
    @abc.abstractmethod
    def elements(self) -> List[models.Element]:
        """Return list of `Element`s"""

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check if `self` is equal to `other`"""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Element must be hashable"""


def queue_search(
    map: models.ElementMap[models.Element],
    queue: queue.Queue["SearchTracker[models.Element]"],
    convert: Callable[[List[models.Element]], "SearchTracker[models.Element]"],
) -> "SearchResult":
    """
    Generic method for traversing through mapped `Element`s
    Input:
        map     : Mapper object linking `Element`s
        queue   : `Queue` object (NOTE: queue instance should be responsible of managing given objects, i.e.
                  raise an Error if objects handled do not conform to a set Signature type)
        convert : Callable that converts list of `Element`s to `SearchTracker` type (for tracking `Element`s traversed)
    Output:
        SearchResult
    """

    @dataclasses.dataclass(frozen=True)
    class _SearchResult:
        solution: List[models.ElementProtocol] = dataclasses.field(default_factory=list)
        searches: Dict[str, "SearchTracker[models.Element]"] = dataclasses.field(
            default_factory=dict
        )

    queue.add(convert([map.start]))
    result = _SearchResult()

    def _check_visited(search: "SearchTracker[models.Element]") -> bool:
        """Check if current tracker has already visited latest `Element`"""
        latest = search.elements[-1]
        return latest in search.elements[:-1]

    def _check_end(search: "SearchTracker[models.Element]") -> bool:
        """Check if search has reach end `Element`"""
        latest = search.elements[-1]
        return latest.uid == map.end.uid

    def _update_searches(search: "SearchTracker[models.Element]") -> None:
        """Update search list in FIFO manner"""
        searches = result.searches
        if search.previous_uid and search.previous_uid in searches:
            del searches[search.previous_uid]
        searches[search.uid] = search

    def _update_solution(search: "SearchTracker[models.Element]") -> None:
        """Populate result with found solution"""
        for e in search.elements:
            result.solution.append(e)

    def _update_queue(search: "SearchTracker[models.Element]") -> None:
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

    return SearchResult(
        solution=result.solution,
        searches={i: s.elements for i, s in enumerate(result.searches.values())},
    )
