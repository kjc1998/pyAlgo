import abc
from typing import Generic, List, Optional
from pyalgo import models
from pyalgo.queue import queue


class PathTracker(Generic[models.Element]):
    """
    Track visited `Element`s
    (NOTE: Wrapper class on top of `Element`, nonetheless still an `Element` with `uid` and `hash` methods)
    Example:
        Input: [1, 4, 7, 8]
        List consists of 4 unique `PathTracker`s
            1) [1]
            2) [1, 4]
            3) [1, 4, 7]
            4) [1, 4, 7, 8]
    """

    def __init__(self, elements: List[models.Element]):
        self.__elements = elements
        self.__post_init()

    @property
    def uid(self) -> str:
        uids = ",".join([e.uid for e in self.__elements])
        return uids

    @property
    def previous_uid(self) -> Optional[str]:
        uids = ",".join([e.uid for e in self.__elements[:-1]])
        return uids if uids else None

    @property
    def elements(self) -> List[models.Element]:
        return self.__elements

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PathTracker) and self.__elements == other.__elements

    def __post_init(self) -> None:
        if len(self.__elements) == 0:
            raise ValueError(
                "can't instantiate search tracker with empty list of `Element`s"
            )


class PathQueue(queue.Queue[PathTracker[models.Element]]):
    """
    Abstract Queue for handling `PathTracker`
    """

    @abc.abstractmethod
    def __len__(self) -> int:
        """Length of queue"""

    @abc.abstractmethod
    def get(self) -> PathTracker[models.Element]:
        """Retrieve `PathTracker` from queue"""

    @abc.abstractmethod
    def add(self, element: PathTracker[models.Element]) -> None:
        """Add `PathTracker` to queue"""

    @abc.abstractmethod
    def remove(self, uid: str) -> None:
        """Remove `PathTracker` from queue based on uid"""
