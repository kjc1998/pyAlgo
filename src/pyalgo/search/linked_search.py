from pyalgo import models
from typing import List, Optional
from typing_extensions import Protocol


class LinkedSearchProtocol(models.ElementProtocol, Protocol[models.Element]):
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
    def previous_uid(self) -> Optional[str]:
        """Return previous `LinkSearch` id"""

    @property
    def elements(self) -> List[models.Element]:
        """Return list of `Element`s"""
