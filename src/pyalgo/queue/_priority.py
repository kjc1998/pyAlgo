from pyalgo import models
from pyalgo.queue import _fifo
from typing import Iterable, List, Optional


class PriorityQueue(_fifo.FIFOQueue[models.WeightedElement]):
    def __init__(
        self,
        elements: Optional[Iterable[models.WeightedElement]] = None,
        heavy: bool = True,
    ) -> None:
        """
        Args:
            elements: Iterables of `WeightedElement`s
            heavy   :
                - True : ↑ weighted elements == ↑ priorities
                - False: ↓ weighted elements == ↑ priorities
        """
        super().__init__(elements)
        self._elements: List[models.WeightedElement] = []
        if elements is not None:
            self._elements = list(elements)
        self.__heavy = heavy

    def add(self, element: models.WeightedElement) -> None:
        """
        Queue elements based on their respective weights.
        """
        inserted = False
        for i, e in enumerate(self._elements):
            insert_heavy = self.__heavy and element.weight > e.weight
            insert_light = not self.__heavy and element.weight < e.weight
            if insert_heavy or insert_light:
                self._elements.insert(i, element)
                inserted = True
                break

        if not inserted:
            super().add(element)
