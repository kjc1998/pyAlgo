import decimal
from typing import Union
from pyalgo import models
from pyalgo.search import path_queue, queue_search


PathTracker = path_queue.PathTracker
Numeric = Union[int, float, decimal.Decimal]


def breadth_first_search(
    map: models.ElementMap[models.Element],
) -> queue_search.SearchResult[models.Element]:
    """
    Perform a Breadth-First Search (DFS) on a given graph from start to end `Element`
    """

    def _convert(tracker: PathTracker[models.Element]) -> Numeric:
        # NOTE: Adjusting weight can achieve different search patterns
        # i.e. for depth-first-search, set the weight to match proportionally with number of elements, ensuring newer elements to be at front
        # in breadth-first-search, set the weight based on levels in reversed order
        return len(tracker.elements)

    queue = path_queue.WeightPathQueue[models.Element](_convert)
    return queue_search.queue_search(map, queue)
