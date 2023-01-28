import abc
import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class Node:
    id: str
    active: bool = False
    visited: bool = False
    parent: Optional["Node"] = None

    def __str__(self):
        if self.active:
            return "X"
        elif self.visited:
            return "1"
        return "0"


class Board(abc.ABC):
    """
    Interface: Handles nodes mapping
    """

    @abc.abstractmethod
    def __str__(self) -> str:
        """String representation of self"""
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Print representation of self"""
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: "Board") -> bool:
        """To compare two board instances"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_sequence(self) -> List["Node"]:
        """Node sequence leading to current active node"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_boards(self) -> List["Board"]:
        """Get next possible boards given current active node"""
        raise NotImplementedError
