import dataclasses
from pyalgo import models
from pyalgo.queue import queue, priority
from pyalgo.search import linked_search
from typing import Any, Callable, Dict, List, Optional

LinkedSearchT = linked_search.LinkedSearchProtocol


def queue_search(
    map: models.ElementMap[models.Element],
    queue: queue.Queue[Any],
    convert: Callable[
        [models.Element, Optional[LinkedSearchT[models.Element]]],
        LinkedSearchT[models.Element],
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
        searches: Dict[str, LinkedSearchT[models.Element]] = dataclasses.field(
            default_factory=dict
        )

    queue.add(convert(map.start, None))
    result = _SearchResult()

    def _check_visited(search: LinkedSearchT[models.Element]) -> bool:
        """Check if current tracker has already visited latest `Element`"""
        latest = search.elements[-1]
        return latest in search.elements[:-1]

    def _check_end(search: LinkedSearchT[models.Element]) -> bool:
        """Check if search has reach end `Element`"""
        latest = search.elements[-1]
        return latest.uid == map.end.uid

    def _update_searches(search: LinkedSearchT[models.Element]) -> None:
        """Update search list in FIFO manner"""
        searches = result.searches
        if search.previous_uid and search.previous_uid in searches:
            del searches[search.previous_uid]
        searches[search.uid] = search

    def _update_solution(search: LinkedSearchT[models.Element]) -> None:
        """Populate result with found solution"""
        for e in search.elements:
            result.solution.append(e)

    def _update_queue(search: LinkedSearchT[models.Element]) -> None:
        """Add `Element` to Queue"""
        elements = search.elements
        for e in map.get_next(elements[-1].uid):
            converted = convert(e, search)
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

    def _convert(
        element: models.Element,
        previous_search: Optional[LinkedSearchT[models.Element]],
    ) -> LinkedSearchT[models.Element]:
        if previous_search is None:
            return linked_search._BasicSearchTracker([element], 0)
        elif isinstance(previous_search, linked_search._BasicSearchTracker):
            # NOTE: Adjusting weight can achieve different search patterns
            # i.e. for depth-first-search, set the weight to match proportionally with number of elements, ensuring newer elements to be at front
            elements = previous_search.elements
            return linked_search._BasicSearchTracker(
                [*elements, element], previous_search.weight - 1
            )
        raise NotImplementedError

    queue = priority.PriorityQueue[linked_search._BasicSearchTracker[models.Element]]()
    return queue_search(map, queue, _convert)
