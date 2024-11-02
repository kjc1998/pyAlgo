from pyalgo import models
from pyalgo.queue import _fifo
from typing import Iterable, List, Optional


class PriorityQueue(_fifo.FIFOQueue[models.WeightedElement]):
    def __init__(
        self, elements: Optional[Iterable[models.WeightedElement]] = None
    ) -> None:
        super().__init__(elements)
        self._elements: List[models.WeightedElement] = []
        if elements is not None:
            self._elements = list(elements)

    def add(self, element: models.WeightedElement) -> None:
        """
        Queue elements based on their respective weights.
        Heavy weighted elements have higher priorities.
        """
        inserted = False
        for i, e in enumerate(self._elements):
            if element > e:
                self._elements.insert(i, element)
                inserted = True
                break
        if not inserted:
            super().add(element)
