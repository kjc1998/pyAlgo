from typing import Iterable, List, Optional
from pyalgo import models
from pyalgo.queue import queue


class SimpleQueue(queue.Queue[models.Element]):
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

    def add(self, element: models.Element) -> None:
        self._elements.append(element)

    def remove(self, uid: str) -> None:
        for i, element in enumerate(self._elements):
            if element.uid == uid:
                del self._elements[i]
                break

    def replace(self, uid: str, element: models.Element) -> None:
        for i, old in enumerate(self._elements):
            if old.uid == uid:
                del self._elements[i]
                self._elements.insert(i, element)
                break
