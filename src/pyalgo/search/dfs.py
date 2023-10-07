from pyalgo import models
from typing import List


def depth_first_search(
    map: models.ElementMap[models.Element],
    start: models.Element,
    end: models.Element,
) -> models.SearchResult:
    """
    Perform a Depth-First Search (DFS) on a given graph from start to end node based on given graph
    """
    if start.uid == end.uid:
        return models.SearchResult([end], {0: [end]})

    visited = set([start])

    def _check_end(search: List[models.Element]) -> bool:
        """Check if last element is equal to end"""
        return search[-1].uid == end.uid

    def _dfs(search: List[models.Element]) -> List[List[models.Element]]:
        """Depth-First Search via recursive lookup from list of `Element` (in order)"""
        if _check_end(search):
            return [search]

        result: List[List[models.Element]] = []
        for e in map.get_next(search[-1].uid):
            if e not in visited:
                visited.add(e)
                result += _dfs([*search, e])
                if _check_end(result[-1]):
                    break
        return result or [search]

    searches = _dfs([start])
    solution = searches[-1] if _check_end(searches[-1]) else []
    return models.SearchResult(solution, {i: s for i, s in enumerate(searches)})
