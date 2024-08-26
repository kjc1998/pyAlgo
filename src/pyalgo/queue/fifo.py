"""
Example:

from pyalgo.queue.fifo import SampleData, FIFOQueue


# NOTE: replace `SampleData` with any data structure of your choice, as long as it complies to `ElementProtocol` [defined in `pyalgo.models`]
e1 = SampleData("1", 5)
e2 = SampleData("1", 6)
queue = PriorityQueue[SampleData]([e1, e2])
"""

import dataclasses
from typing import Any, Iterable, List, Optional
from pyalgo import models
from pyalgo.queue import queue


@dataclasses.dataclass
class SampleData:
    uid: str
    value: Any


class FIFOQueue(queue.Queue[models.Element]):
    """First-In, First-Out"""

    def __init__(self, elements: Optional[Iterable[models.Element]] = None) -> None:
        self._elements: List[models.Element] = []
        if elements is not None:
            self._elements = list(elements)

    def __len__(self) -> int:
        return len(self._elements)

    def get(self) -> models.Element:
        try:
            result = self._elements.pop(0)
        except IndexError:
            raise queue.EmptyQueueError()

        return result

    def add(self, element: Any) -> None:
        self._elements.append(element)

    def remove(self, uid: str) -> None:
        checked = False
        for i, element in enumerate(self._elements):
            if element.uid == uid:
                del self._elements[i]
                checked = True
                break
        if not checked:
            raise KeyError("no such uid stored")
