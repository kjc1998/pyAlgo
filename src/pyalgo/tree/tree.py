import abc
from pyalgo import node
from pyalgo.models import Comparable as C
from typing import Generic, Optional, Sequence, Tuple

Node = node.Node
NodeMap = Tuple[C, Sequence[C]]


class Tree(abc.ABC, Generic[C]):
    @property
    @abc.abstractmethod
    def root(self) -> Optional[Node[C]]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def height(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def mappings(self) -> Sequence[NodeMap[C]]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item: C) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, item: C) -> None:
        raise NotImplementedError
