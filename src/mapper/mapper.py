import abc
from typing import List, Optional


class Node:
    def __init__(self, uid: str):
        self._uid = uid
        self._visited = False
        self._active = False
        self._parent = None

    # Properties
    @property
    def uid(self) -> str:
        return self._uid

    @property
    def active(self) -> bool:
        return self._active

    @property
    def visited(self) -> bool:
        return self._visited

    @property
    def parent(self) -> Optional["Node"]:
        return self._parent

    # Dunder methods
    def __str__(self) -> str:
        if self.active:
            return "X"
        elif self.visited:
            return "1"
        return "0"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Node)
            and self.uid == other.uid
            and self.active == other.active
            and self.visited == other.visited
            and self.parent == other.parent
        )

    def __repr__(self) -> str:
        return f"Node({self.uid}, {str(self)})"

    def set_active(self, parent_node: Optional["Node"] = None) -> None:
        if self._visited or self._active:
            raise ValueError(f"Node({self.uid}) has been set active before")
        self._active = True
        self._visited = True
        self._parent = parent_node

    def unset_active(self) -> None:
        if not self._active:
            raise ValueError(f"Node({self.uid}) is no longer active")
        self._active = False


class Mapper(abc.ABC):
    """
    Handles mapping of `Node`s (auto filter visited `Node`s)
    """

    @abc.abstractmethod
    def get_next_uids(self, node_id: str, visited_uids: List[str]) -> List["Node"]:
        """Return possible paths for a specified `Node` given the visited uids"""
        pass
