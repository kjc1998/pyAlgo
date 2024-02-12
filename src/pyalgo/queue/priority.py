"""
Example:

from pyalgo.queue.priority import SampleData, PriorityQueue


# NOTE: replace `SampleData` with any data structure of your choice, as long as it complies to `WeightedElementProtocol` [defined in `pyalgo.models`]
e1 = SampleData("1", 5)
e2 = SampleData("1", 6)
queue = PriorityQueue[SampleData]([e1, e2])
"""

import dataclasses
from pyalgo import models
from pyalgo.queue import fifo
from typing import Iterable, List, Optional


@dataclasses.dataclass(frozen=True)
class SampleData:
    uid: str
    value: int

    @property
    def weight(self) -> int:
        return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value < other.value
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value <= other.value
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value > other.value
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value >= other.value
        return False


class PriorityQueue(fifo.FIFOQueue[models.WeightedElement]):
    def __init__(
        self, elements: Optional[Iterable[models.WeightedElement]] = None
    ) -> None:
        super().__init__(elements)
        self._elements: List[models.WeightedElement] = []
        if elements is not None:
            self._elements = list(elements)

    def add(self, element: models.WeightedElement) -> None:
        inserted = False
        for i, e in enumerate(self._elements):
            if element > e:
                self._elements.insert(i, element)
                inserted = True
                break
        if not inserted:
            super().add(element)
