import decimal
from pyalgo import models
from pyalgo.queue import priority
from pyalgo.search import queue_search, bfs
from typing import List, Union


class _DFSSearchTracker(bfs._BFSSearchTracker[models.Element]):
    def __init__(self, elements: List[models.Element]):
        super().__init__(elements)
        self.__elements = elements

    @property
    def weight(self) -> Union[int, float, decimal.Decimal]:
        """
        Weightage is dependent on number of elements stored.
        The greater the number, the higher its priority.
        """
        return len(self.__elements)


def depth_first_search(
    map: models.ElementMap[models.Element],
) -> queue_search.SearchResult:
    """
    Perform a Depth-First Search (DFS) on a given graph from start to end `Element`
    """

    queue = priority.PriorityQueue[_DFSSearchTracker[models.Element]]()
    return queue_search.queue_search(map, queue, lambda x: _DFSSearchTracker(x))
