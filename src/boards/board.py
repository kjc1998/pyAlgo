import abc
import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class Node:
    id: str
    active: bool = False
    visited: bool = False
    parent: Optional["Node"] = None


class Board(abc.ABC):
    """
    Interface: Handles nodes mapping
    """

    def get_sequence(self) -> List["Node"]:
        """Node sequence leading to current active node"""
        raise NotImplementedError

    def get_next_boards(self) -> List["Board"]:
        """Get next possible boards given current active node"""
        raise NotImplementedError
