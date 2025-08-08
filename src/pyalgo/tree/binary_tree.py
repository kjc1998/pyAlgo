from pyalgo import node
from pyalgo.tree import tree
from pyalgo.models import Comparable as C
from pyalgo.tree.tree import Node
from typing import Optional, Tuple


class BinaryTree(tree.Tree[C]):
    def __init__(self, *items: C) -> None:
        self.__root: Optional[Node[C]] = None
        for item in items:
            self.add(item)

    @property
    def root(self) -> Optional[Node[C]]:
        return self.__root if self.__root else None

    def add(self, item: C) -> None:
        item_node = node.Node(item)
        if self.root is None:
            self.__root = item_node
            return None
        self.__binary_add(self.root, item_node)

    def __binary_add(self, base: Node[C], node: Node[C]) -> None:
        left, right = self.__left_right(base)
        if left and node.item < base.item:
            self.__binary_add(left, node)
        elif right and node.item >= base.item:
            self.__binary_add(right, node)
        else:
            base.add_children(node)

    @staticmethod
    def __left_right(base: Node[C]) -> Tuple[Optional[Node[C]], Optional[Node[C]]]:
        children = sorted(base.children, key=lambda x: x.item)
        if len(children) == 2:
            return (children[0], children[1])
        if len(children) == 1:
            child = children[0]
            return (child, None) if child.item < base.item else (None, child)
        return (None, None)
