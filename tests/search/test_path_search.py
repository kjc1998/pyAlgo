import pytest
import dataclasses
from typing import Dict, List, Union
from pyalgo import models, search
from pyalgo.search import queue_search


@dataclasses.dataclass(frozen=True)
class Element:
    uid: str
    weight: Union[int, float]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.uid == other.uid and self.weight == other.weight
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


@pytest.mark.parametrize("search", [search.dijakstra_search])
@pytest.mark.parametrize(
    "graph, start, expected",
    [
        pytest.param(
            {"end": []},
            Element("end", 0),
            queue_search.SearchResult([Element("end", 0)], {0: [Element("end", 0)]}),
            id="start_eq_end_case",
        ),
        pytest.param(
            {
                "1": [Element("2", 2), Element("3", 7)],
                "2": [Element("4", 3), Element("5", 4)],
                "3": [Element("end", 0), Element("6", 2)],
                "4": [],
                "5": [],
            },
            Element("1", 0),
            queue_search.SearchResult(
                [Element("1", 0), Element("3", 7), Element("end", 0)],
                {
                    0: [Element("1", 0), Element("2", 2), Element("4", 3)],
                    1: [Element("1", 0), Element("2", 2), Element("5", 4)],
                    2: [Element("1", 0), Element("3", 7), Element("end", 0)],
                },
            ),
            id="standard_case",
        ),
    ],
)
def test_common_search(search, graph, start, expected):
    end = Element("end", 0)
    map = SimpleMap(start, end, graph)
    observed = search(map)
    assert observed == expected
