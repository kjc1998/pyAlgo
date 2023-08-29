from typing import Generic, Iterable, List, Optional
from pyalgo import models
from pyalgo.queue import queue


class EmptyQueueError(ValueError):
    def __init__(self):
        message = "cannot get element from empty queue"
        super().__init__(message)


class SimpleQueue(queue.Queue, Generic[models.Element]):
    def __init__(self, elements: Optional[Iterable[models.Element]] = None):
        self._elements: List[models.Element] = []
        if elements is not None:
            self._elements = list(elements)

    def get(self) -> models.Element:
        try:
            result = self._elements.pop(0)
        except IndexError:
            raise EmptyQueueError()

        return result

    def add(self, element: models.Element) -> None:
        self._elements.append(element)

    def remove(self, uid: str) -> None:
        for i, element in enumerate(self._elements):
            if element.uid == uid:
                del self._elements[i]
                break

    def replace(self, uid: str, element: models.Element) -> None:
        pass
