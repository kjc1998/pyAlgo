import abc
from pyalgo import models
from typing import List, Optional, Generic


class SearchTracker(abc.ABC, Generic[models.Element]):
    """
    Search `Element`s Chaining
    (NOTE: Wrapper class on top of `Element`, nonetheless still an `Element` with `uid` and `hash` methods)
    Example:
        Input: [1, 4, 7, 8]
        List consists of 4 unique `LinkSearch`s
            1) [1]
            2) [1, 4]
            3) [1, 4, 7]
            4) [1, 4, 7, 8]
    """
    @property
    @abc.abstractmethod
    def uid(self) -> str:
        """Return Element's unique id"""

    @property
    @abc.abstractmethod
    def previous_uid(self) -> Optional[str]:
        """Return previous `LinkSearch` id"""

    @property
    @abc.abstractmethod
    def elements(self) -> List[models.Element]:
        """Return list of `Element`s"""
    
    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check if `self` is equal to `other`"""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Element must be hashable"""

