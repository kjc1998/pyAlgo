import pytest
import dataclasses
from typing import Dict, List
from pyalgo import models
from pyalgo.search import dfs, bfs


@dataclasses.dataclass(frozen=True)
class Element:
    uid: str


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


@pytest.mark.parametrize("search", [dfs.depth_first_search, bfs.breadth_first_search])
@pytest.mark.parametrize(
    "graph, start, expected",
    [
        pytest.param(
            {"end": []},
            Element("end"),
            models.SearchResult([Element("end")], {0: [Element("end")]}),
            id="start_eq_end_case",
        ),
        pytest.param(
            {
                "1": [Element("2"), Element("3")],
                "2": [Element("4"), Element("5")],
                "3": [Element("end"), Element("6")],  # element 6 won't be assessed
                "4": [],
                "5": [],
            },
            Element("1"),
            models.SearchResult(
                [Element("1"), Element("3"), Element("end")],
                {
                    0: [Element("1"), Element("2"), Element("4")],
                    1: [Element("1"), Element("2"), Element("5")],
                    2: [Element("1"), Element("3"), Element("end")],
                },
            ),
            id="standard_case",
        ),
        pytest.param(
            {
                "1": [Element("2"), Element("3")],
                "2": [Element("4")],
                "3": [Element("5"), Element("6"), Element("7")],
                "4": [],
                "5": [],
                "6": [],
                "7": [],
            },
            Element("1"),
            models.SearchResult(
                [],
                {
                    0: [Element("1"), Element("2"), Element("4")],
                    1: [Element("1"), Element("3"), Element("5")],
                    2: [Element("1"), Element("3"), Element("6")],
                    3: [Element("1"), Element("3"), Element("7")],
                },
            ),
            id="no_solution_case",
        ),
        pytest.param(
            {
                "1": [Element("2"), Element("3")],
                "2": [Element("4"), Element("6")],
                "3": [Element("5"), Element("end")],
                "4": [Element("2")],
                "5": [],
                "6": [],
            },
            Element("1"),
            models.SearchResult(
                [Element("1"), Element("3"), Element("end")],
                {
                    0: [Element("1"), Element("2"), Element("4")],
                    1: [Element("1"), Element("2"), Element("6")],
                    2: [Element("1"), Element("3"), Element("5")],
                    3: [Element("1"), Element("3"), Element("end")],
                },
            ),
            id="cyclic_case",
        ),
        pytest.param(
            {"1": [Element("2")], "2": [Element("3")], "3": [Element("1")]},
            Element("1"),
            models.SearchResult([], {0: [Element("1"), Element("2"), Element("3")]}),
            id="cyclic_no_solution_case",
        ),
    ],
)
def test_common_search(search, graph, start, expected):
    end = Element("end")
    map = SimpleMap(start, end, graph)
    observed = search(map)
    assert observed == expected


@pytest.mark.parametrize(
    "search, expected",
    [
        pytest.param(
            dfs.depth_first_search,
            models.SearchResult(
                [Element("1"), Element("2"), Element("5"), Element("end")],
                {
                    0: [Element("1"), Element("2"), Element("4"), Element("7")],
                    1: [
                        Element("1"),
                        Element("2"),
                        Element("5"),
                        Element("8"),
                        Element("10"),
                    ],
                    2: [Element("1"), Element("2"), Element("5"), Element("end")],
                },
            ),
            id="dfs_case",
        ),
        pytest.param(
            bfs.breadth_first_search,
            models.SearchResult(
                [Element("1"), Element("2"), Element("5"), Element("end")],
                {
                    0: [Element("1"), Element("2"), Element("6")],
                    1: [Element("1"), Element("3"), Element("7")],
                    2: [Element("1"), Element("2"), Element("4"), Element("7")],
                    3: [Element("1"), Element("2"), Element("5"), Element("8")],
                    4: [Element("1"), Element("2"), Element("5"), Element("end")],
                },
            ),
            id="bfs_case",
        ),
    ],
)
def test_complicated_case(search, expected):
    map = SimpleMap(
        Element("1"),
        Element("end"),
        {
            "1": [Element("2"), Element("3")],
            "2": [Element("4"), Element("5"), Element("6")],
            "3": [Element("7")],
            "4": [Element("7")],
            "5": [Element("8"), Element("end")],
            "6": [Element("9")],
            "7": [],
            "8": [Element("10")],
            "9": [],
            "10": [],
        },
    )
    observed = search(map)
    assert observed == expected
