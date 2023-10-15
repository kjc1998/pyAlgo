from pyalgo import models
from pyalgo.queue import priority
from pyalgo.search import linked_search, bfs
from typing import Optional

LinkedSearchT = linked_search.LinkedSearchProtocol


def dijakstra_search(
    map: models.ElementMap[models.WeightedElement],
) -> models.SearchResult:
    """
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    Subset of breadth-first-search, with minor tweaks around weightage assignment
    """

    def _convert(
        element: models.WeightedElement,
        previous_search: Optional[LinkedSearchT[models.WeightedElement]],
    ) -> LinkedSearchT[models.WeightedElement]:
        if previous_search is None:
            return linked_search._DijakstraPathTracker([element])
        elif isinstance(previous_search, linked_search._DijakstraPathTracker):
            elements = previous_search.elements
            return linked_search._DijakstraPathTracker([*elements, element])
        raise NotImplementedError

    queue = priority.PriorityQueue[
        linked_search._DijakstraPathTracker[models.WeightedElement]
    ]()
    return bfs.queue_search(map, queue, _convert)
