import abc
import dataclasses
from pyalgo import models
from pyalgo.queue import queue as queue_
from typing import Any, Callable, Dict, Iterable, List, Optional, Generic


@dataclasses.dataclass
class SearchResult:
    """
    Search Result Model
    solution:   List of `Element`s from start to end
    paths:   Dict of paths done in order from 0 to n-1
    """

    solution: Iterable[models.ElementProtocol] = dataclasses.field(default_factory=list)
    paths: Dict[int, Iterable[models.ElementProtocol]] = dataclasses.field(
        default_factory=dict
    )


class PathTracker(abc.ABC, Generic[models.Element]):
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
    queue: queue_.Queue[Any],
    convert: Callable[[List[models.Element]], "PathTracker[models.Element]"],
) -> "SearchResult":
    """
    Generic method for traversing through mapped `Element`s
    Input:
        map     : Mapper object linking `Element`s
        queue   : `Queue` object (NOTE: queue instance should be responsible of managing given objects, i.e.
                  raise an Error if objects handled do not conform to a set Signature type)
        convert : Callable that converts list of `Element`s to `PathTracker` type (for tracking `Element`s traversed)
    Output:
        SearchResult
    """

    queue.add(convert([map.start]))

    solution: List[models.Element] = []
    searches: Dict[str, "PathTracker[models.Element]"] = {}

    def _check_visited(path: "PathTracker[models.Element]") -> bool:
        """Check if current tracker has already visited latest `Element`"""
        latest = path.elements[-1]
        return latest in path.elements[:-1]

    def _check_end(path: "PathTracker[models.Element]") -> bool:
        """Check if path has reach end `Element`"""
        latest = path.elements[-1]
        return latest.uid == map.end.uid

    def _update_searches(path: "PathTracker[models.Element]") -> None:
        """Update search list in FIFO manner"""
        if path.previous_uid and path.previous_uid in searches:
            del searches[path.previous_uid]
        searches[path.uid] = path

    def _update_queue(path: "PathTracker[models.Element]") -> None:
        """Add `Element` to Queue"""
        elements = path.elements
        for e in map.get_next(elements[-1].uid):
            converted = convert([*path.elements, e])
            queue.add(converted)

    while len(queue) > 0:
        path = queue.get()
        if not _check_visited(path):
            _update_searches(path)
            if _check_end(path):
                solution = [*path.elements]
                break
            _update_queue(path)

    return SearchResult(
        solution=solution,
        paths={i: s.elements for i, s in enumerate(searches.values())},
    )
