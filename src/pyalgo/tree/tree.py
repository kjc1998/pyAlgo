import abc
from pyalgo import node
from pyalgo.models import Comparable as C
from typing import Generic, Optional

Node = node.Node


class Tree(abc.ABC, Generic[C]):
    @property
    @abc.abstractmethod
    def root(self) -> Optional[Node[C]]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item: C) -> None:
        raise NotImplementedError
