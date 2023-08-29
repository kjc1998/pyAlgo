import abc
from typing import Generic
from pyalgo import models


class Queue(abc.ABC, Generic[models.Element]):
    @abc.abstractmethod
    def get(self) -> models.Element:
        """Retrieve `Element` from queue"""

    @abc.abstractmethod
    def add(self, element: models.Element) -> None:
        """Add `Element` to queue"""

    @abc.abstractmethod
    def remove(self, uid: str) -> None:
        """Remove `Element` from queue based on uid"""

    @abc.abstractmethod
    def replace(self, uid: str, element: models.Element) -> None:
        """Replace `Element` based on uid"""
