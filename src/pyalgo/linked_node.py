from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class LinkedNode(Generic[T]):
    def __init__(self, element: T) -> None:
        self.__element = element
        self.__parent: Optional["LinkedNode[T]"] = None
        self.__children: List["LinkedNode[T]"] = []

    @property
    def element(self) -> T:
        return self.__element

    @property
    def parent(self) -> Optional["LinkedNode[T]"]:
        return self.__parent

    @property
    def children(self) -> List["LinkedNode[T]"]:
        return self.__children

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.element == other.element
            and self.parent == other.parent
            and self.children == other.children
        )

    def set_parent(self, parent: "LinkedNode[T]") -> None:
        if not self.__relationship_exists(parent, self):
            self.__parent = parent
            parent.add_children(self)

    def remove_parent(self) -> None:
        parent = self.__parent
        if parent is not None:
            self.__parent = None
            parent.remove_children(self)

    def add_children(self, *children: "LinkedNode[T]") -> None:
        for child in children:
            if not self.__relationship_exists(self, child):
                self.__children.append(child)
                child.set_parent(self)

    def remove_children(self, *children: "LinkedNode[T]") -> None:
        for child in children:
            if child in self.children:
                self.children.remove(child)
                child.remove_parent()

    def __relationship_exists(
        self, parent: "LinkedNode[T]", child: "LinkedNode[T]"
    ) -> bool:
        if child.parent == parent and child in parent.children:
            return True
        return False
