import decimal
from pyalgo import models
from pyalgo.queue import priority
from pyalgo.search import linked_search, bfs
from typing import List, Union

LinkedSearchT = linked_search.LinkedSearchProtocol


class _DijakstraPathTracker(bfs._BasicSearchTracker[models.WeightedElement]):
    def __init__(self, elements: List[models.WeightedElement]):
        super().__init__(elements)

    @property
    def weight(self) -> Union[int, float, decimal.Decimal]:
        return sum([e.weight for e in self.__elements])


def dijakstra_search(
    map: models.ElementMap[models.WeightedElement],
) -> models.SearchResult:
    """
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    Subset of breadth-first-search, with minor tweaks around weightage assignment
    """

    queue = priority.PriorityQueue[_DijakstraPathTracker[models.WeightedElement]]()
    return bfs.queue_search(map, queue, lambda x: _DijakstraPathTracker(x))
