from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class LinkedNode(Generic[T]):
    def __init__(self, element: T) -> None:
        self.element = element
        self.parent: Optional["LinkedNode[T]"] = None
        self.children: List["LinkedNode[T]"] = []

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.element == other.element
            and self.parent == other.parent
            and self.children == other.children
        )

    def set_parent(self, parent: "LinkedNode[T]") -> None:
        self.__establish_link(parent, self)

    def remove_parent(self) -> None:
        if self.parent:
            self.__destroy_link(self.parent, self)

    def add_children(self, *children: "LinkedNode[T]") -> None:
        for child in children:
            self.__establish_link(self, child)

    def remove_children(self, *children: "LinkedNode[T]") -> None:
        for child in children:
            self.__destroy_link(self, child)

    def unlink(self) -> None:
        parent = self.parent
        children = [i for i in self.children]
        self.remove_parent()
        self.remove_children(*children)
        if parent:
            parent.add_children(*children)

    def __destroy_link(self, parent: "LinkedNode[T]", child: "LinkedNode[T]") -> None:
        if self.__link_exists(parent, child):
            child.parent = None
            parent.children.remove(child)

    def __establish_link(self, parent: "LinkedNode[T]", child: "LinkedNode[T]") -> None:
        if not self.__link_exists(parent, child):
            child.parent = parent
            parent.children.append(child)

    def __link_exists(self, parent: "LinkedNode[T]", child: "LinkedNode[T]") -> bool:
        if child.parent == parent and child in parent.children:
            return True
        return False
