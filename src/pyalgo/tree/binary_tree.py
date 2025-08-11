from pyalgo import node
from pyalgo.tree import tree
from pyalgo.models import Comparable as C
from pyalgo.tree.tree import Node, NodeMap
from typing import List, Optional, Sequence, Tuple


class BinaryTree(tree.Tree[C]):
    def __init__(self, *items: C) -> None:
        self.__root: Optional[Node[C]] = None
        for item in items:
            self.add(item)

    @property
    def root(self) -> Optional[Node[C]]:
        return self.__root if self.__root else None

    @property
    def height(self) -> int:
        def get_height(node: Node[C]) -> int:
            left, right = self.__left_right(node)
            left_height = get_height(left) if left else 0
            right_height = get_height(right) if right else 0
            return 1 + max(left_height, right_height)

        return get_height(self.root) if self.root else 0

    @property
    def mappings(self) -> List[NodeMap[C]]:
        def get_mappings(node: Node[C]) -> List[NodeMap[C]]:
            left, right = self.__left_right(node)
            result: List[NodeMap[C]] = [
                (node.item, [i.item for i in [left, right] if i is not None]),
            ]
            result += get_mappings(left) if left else []
            result += get_mappings(right) if right else []
            return result

        return get_mappings(self.root) if self.root else []

    def add(self, item: C) -> None:
        item_node = node.Node(item)
        if self.root is None:
            self.__root = item_node
            return None
        self.__binary_add(self.root, item_node)

    def remove(self, item: C) -> None:
        if not self.root:
            raise ValueError(f"No such item in tree: {item}")

        node = self.__binary_get(self.root, item)
        parent, children = self.__unlink(node)
        if parent:
            for child in children:
                self.__binary_add(parent, child)
        else:
            self.__assign_root(children)

    def __assign_root(self, children: Sequence[Node[C]]) -> None:
        self.__root = None
        for child in children:
            if self.root is None:
                self.__root = child
            else:
                self.__binary_add(self.root, child)

    def __binary_get(self, base: Optional[Node[C]], item: C) -> Node[C]:
        if base is None:
            raise ValueError(f"No such item in tree: {item}")
        if base.item == item:
            return base

        left, right = self.__left_right(base)
        if item < base.item:
            return self.__binary_get(left, item)
        return self.__binary_get(right, item)

    def __binary_add(self, base: Node[C], node: Node[C]) -> None:
        left, right = self.__left_right(base)
        if left and node.item < base.item:
            self.__binary_add(left, node)
        elif right and node.item >= base.item:
            self.__binary_add(right, node)
        else:
            base.add_children(node)

    def __unlink(self, base: Node[C]) -> Tuple[Optional[Node[C]], Sequence[Node[C]]]:
        parent = base.parents[0] if base.parents else None
        children = tuple(c for c in self.__left_right(base) if c is not None)
        base.remove_parents(*base.parents)
        base.remove_children(*base.children)
        return parent, children

    @staticmethod
    def __left_right(base: Node[C]) -> Tuple[Optional[Node[C]], Optional[Node[C]]]:
        children = sorted(base.children, key=lambda x: x.item)
        if len(children) == 2:
            return (children[0], children[1])
        if len(children) == 1:
            child = children[0]
            return (child, None) if child.item < base.item else (None, child)
        return (None, None)
