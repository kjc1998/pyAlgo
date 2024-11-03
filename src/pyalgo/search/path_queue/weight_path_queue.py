import dataclasses
import decimal
from typing import Callable, Generic, Union
from pyalgo import models, queue
from pyalgo.search.path_queue import path_queue

Numeric = Union[int, float, decimal.Decimal]


@dataclasses.dataclass
class _WeightTracker(Generic[models.Element]):
    """
    Model complying to `WeightedElement` structure
    to arrange trackers based on weights
    """

    uid: str
    weight: Numeric
    tracker: path_queue.PathTracker[models.Element]


class WeightPathQueue(path_queue.PathQueue[models.Element]):
    """
    Queue in charge of managing `PathTracker`s based on weights.
    NOTE: Weights are assigned via `converter` callable
    """

    def __init__(
        self,
        convert: Callable[[path_queue.PathTracker[models.Element]], Numeric],
    ) -> None:
        self.__queue = queue.PriorityQueue["_WeightTracker[models.Element]"](
            heavy=False
        )
        self.__convert = convert

    def __len__(self) -> int:
        return len(self.__queue)

    def get(self) -> path_queue.PathTracker[models.Element]:
        item = self.__queue.get()
        return item.tracker

    def add(self, element: path_queue.PathTracker[models.Element]) -> None:
        item = _WeightTracker(
            uid=element.uid,
            weight=self.__convert(element),
            tracker=element,
        )
        self.__queue.add(item)

    def remove(self, uid: str) -> None:
        self.__queue.remove(uid)
