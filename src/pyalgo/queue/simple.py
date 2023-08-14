from typing import Dict, Generic, Iterable, List, Optional
from pyalgo.queue import queue


class EmptyQueueError(ValueError):
    def __init__(self):
        message = "cannot get element from empty queue"
        super().__init__(message)


class SimpleQueue(queue.Queue, Generic[queue.Element]):
    def __init__(self, elements: Optional[Iterable[queue.Element]] = None):
        self._elements: List[queue.Element]
        self._uid_lookup: Dict[str, int]

        if elements is None:
            self._elements = []
            self._uid_lookup = {}
        else:
            self._elements = list(elements)
            self._uid_lookup = {e.uid: i for i, e in enumerate(self._elements)}

    def get(self) -> queue.Element:
        try:
            result = self._elements.pop(0)
        except IndexError:
            raise EmptyQueueError()

        del self._uid_lookup[result.uid]
        return result

    def add(self, element: queue.Element) -> None:
        self._elements.append(element)
        self._uid_lookup[element.uid] = len(self._elements) - 1

    def remove(self, uid: str) -> None:
        pass

    def replace(self, uid: str, element: queue.Element) -> None:
        pass
