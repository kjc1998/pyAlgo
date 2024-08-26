import pytest
import dataclasses
from typing import Dict, List, Union
from pyalgo import models
from pyalgo.search import queue_search, dijakstra


@dataclasses.dataclass(frozen=True)
class Element:
    uid: str
    weight: Union[int, float]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight == other.weight
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight < other.weight
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight <= other.weight
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight > other.weight
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.weight >= other.weight
        return False


class SimpleMap(models.ElementMap["Element"]):
    def __init__(
        self, start: "Element", end: "Element", graph: Dict[str, List["Element"]]
    ):
        self._start = start
        self._end = end
        self._graph = graph

    @property
    def start(self) -> "Element":
        return self._start

    @property
    def end(self) -> "Element":
        return self._end

    def get_next(self, uid: str) -> List["Element"]:
        return self._graph[uid]


@pytest.mark.parametrize("search", [dijakstra.dijakstra_search])
@pytest.mark.parametrize(
    "graph, start, expected",
    [
        pytest.param(
            {"end": []},
            Element("end", 0),
            queue_search.SearchResult([Element("end", 0)], {0: [Element("end", 0)]}),
            id="start_eq_end_case",
        )
    ],
)
def test_common_search(search, graph, start, expected):
    end = Element("end", 0)
    map = SimpleMap(start, end, graph)
    observed = search(map)
    assert observed == expected
