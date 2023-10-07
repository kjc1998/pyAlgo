import pytest
import dataclasses
from typing import Dict, List
from pyalgo import models
from pyalgo.search import dfs


@dataclasses.dataclass(frozen=True)
class Element:
    uid: str


class SimpleMap(models.ElementMap["Element"]):
    def __init__(self, graph: Dict[str, List["Element"]]):
        self._graph = graph

    def get_next(self, uid: str) -> List["Element"]:
        return self._graph[uid]


@pytest.mark.parametrize(
    "map, start, expected",
    [
        pytest.param(
            SimpleMap({"end": []}),
            Element("end"),
            models.SearchResult([Element("end")], {0: [Element("end")]}),
            id="start_eq_end_case",
        ),
        pytest.param(
            SimpleMap(
                {
                    "1": [Element("2"), Element("3")],
                    "2": [Element("4"), Element("5")],
                    "3": [Element("end"), Element("6")],  # element 6 won't be assessed
                    "4": [],
                    "5": [],
                }
            ),
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
            SimpleMap(
                {
                    "1": [Element("2"), Element("3")],
                    "2": [Element("4")],
                    "3": [Element("5"), Element("6"), Element("7")],
                    "4": [],
                    "5": [],
                    "6": [],
                    "7": [],
                }
            ),
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
            SimpleMap(
                {
                    "1": [Element("2"), Element("3")],
                    "2": [Element("4"), Element("6")],
                    "3": [Element("5"), Element("end")],
                    "4": [Element("2")],
                    "5": [Element("6")],
                    "6": [],
                }
            ),
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
    ],
)
def test_depth_first_search(map, start, expected):
    end = Element("end")
    observed = dfs.depth_first_search(map, start, end)
    assert observed == expected
