import abc
from typing import Generic
from pyalgo import models


class EmptyQueueError(ValueError):
    def __init__(self) -> None:
        message = "cannot get element from empty queue"
        super().__init__(message)


class Queue(abc.ABC, Generic[models.Element]):
    @abc.abstractmethod
    def __len__(self) -> int:
        """Length of queue"""

    @abc.abstractmethod
    def get(self) -> models.Element:
        """Retrieve `Element` from queue"""

    @abc.abstractmethod
    def add(self, element: models.Element) -> None:
        """Add `Element` to queue"""

    @abc.abstractmethod
    def remove(self, uid: str) -> None:
        """Remove `Element` from queue based on uid"""
