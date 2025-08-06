from typing import Generic, List, TypeVar, Sequence

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, item: T):
        self.__item = item
        self.__parents: List["Node[T]"] = []
        self.__children: List["Node[T]"] = []

    @property
    def item(self) -> T:
        return self.__item

    @property
    def parents(self) -> Sequence["Node[T]"]:
        return tuple(self.__parents)

    @property
    def children(self) -> Sequence["Node[T]"]:
        return tuple(self.__children)

    def __repr__(self) -> str:
        return f"Node({self.item})"

    def add_children(self, *children: "Node[T]") -> None:
        for child in children:
            self.__link(self, child)

    def remove_children(self, *children: "Node[T]") -> None:
        for child in children:
            self.__unlink(self, child)

    def add_parents(self, *parents: "Node[T]") -> None:
        for parent in parents:
            self.__link(parent, self)

    def remove_parents(self, *parents: "Node[T]") -> None:
        for parent in parents:
            self.__unlink(parent, self)

    def __link(self, parent: "Node[T]", child: "Node[T]") -> None:
        if parent == self and child not in self.children:
            self.__children.append(child)
            child.add_parents(self)
        if child == self and parent not in self.parents:
            self.__parents.append(parent)
            parent.add_children(self)

    def __unlink(self, parent: "Node[T]", child: "Node[T]") -> None:
        if parent == self and child in self.children:
            self.__children.remove(child)
            child.remove_parents(self)
        if child == self and parent in self.parents:
            self.__parents.remove(parent)
            parent.remove_children(self)
