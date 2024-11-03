import decimal
from typing import Union
from pyalgo import models
from pyalgo.search import path_queue, queue_search

PathTracker = path_queue.PathTracker
Numeric = Union[int, float, decimal.Decimal]


def dijakstra_search(
    map: models.ElementMap[models.WeightedElement],
) -> queue_search.SearchResult[models.WeightedElement]:
    """
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    Subset of breadth-first-search, with minor tweaks around weightage assignment
    """

    def _convert(tracker: PathTracker[models.WeightedElement]) -> Numeric:
        # NOTE: Adjusting weight can achieve different search patterns
        # i.e. for depth-first-search, set the weight to match proportionally with number of elements, ensuring newer elements to be at front
        # in breadth-first-search, set the weight based on levels in reversed order
        return sum([e.weight for e in tracker.elements])

    queue = path_queue.WeightPathQueue[models.WeightedElement](_convert)
    return queue_search.queue_search(map, queue)
