import abc
from pyalgo.models import Numbers, WeightedElement
from typing import Dict, Generic, List


class Tree(abc.ABC, Generic[WeightedElement]):
    """Tree Data Structure for organising `Element`"""

    @abc.abstractmethod
    def insert(self, element: WeightedElement) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, weight: Numbers) -> WeightedElement:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, weight: Numbers) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_mapping(self) -> Dict[WeightedElement, List[WeightedElement]]:
        raise NotImplementedError
