import dataclasses
from typing import Dict, Generic, Iterable, List
from pyalgo import models
from pyalgo.search.path_queue import path_queue


@dataclasses.dataclass
class SearchResult(Generic[models.Element]):
    """
    Search Result Model
    solution:   List of `Element`s from start to end
    searches:   Dict of paths done in order from 0 to n-1
    """

    solution: Iterable[models.Element] = dataclasses.field(default_factory=list)
    searches: Dict[int, Iterable[models.Element]] = dataclasses.field(
        default_factory=dict
    )


def queue_search(
    map: models.ElementMap[models.Element],
    queue: path_queue.PathQueue[models.Element],
) -> "SearchResult[models.Element]":
    """
    Generic method for traversing through mapped `Element`s
    Input:
        map     : Mapper object linking `Element`s
        queue   : `PathQueue` object
    Output:
        SearchResult
    """

    queue.add(path_queue.PathTracker([map.start]))

    solution: List[models.Element] = []
    searches: Dict[str, path_queue.PathTracker[models.Element]] = {}

    def _check_visited(path: path_queue.PathTracker[models.Element]) -> bool:
        """Check if current tracker has already visited latest `Element`"""
        latest = path.elements[-1]
        return latest in path.elements[:-1]

    def _check_end(path: path_queue.PathTracker[models.Element]) -> bool:
        """Check if path has reach end `Element`"""
        latest = path.elements[-1]
        return latest.uid == map.end.uid

    def _update_searches(path: path_queue.PathTracker[models.Element]) -> None:
        """Update search list in FIFO manner"""
        if path.previous_uid and path.previous_uid in searches:
            del searches[path.previous_uid]
        searches[path.uid] = path

    def _update_queue(path: path_queue.PathTracker[models.Element]) -> None:
        """Add `Element` to Queue"""
        elements = path.elements
        for e in map.get_next(elements[-1].uid):
            tracker = path_queue.PathTracker([*path.elements, e])
            queue.add(tracker)

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
        searches={i: s.elements for i, s in enumerate(searches.values())},
    )
