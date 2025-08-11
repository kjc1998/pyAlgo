from pyalgo import node
from pyalgo.tree import tree
from pyalgo.models import Comparable as C
from pyalgo.tree.tree import Node, NodeMap
from typing import Generic, List, Optional, Sequence, Tuple


class _BinaryTreeHandler(Generic[C]):
    @staticmethod
    def left_right(base: Node[C]) -> Tuple[Optional[Node[C]], Optional[Node[C]]]:
        children = sorted(base.children, key=lambda x: x.item)
        if len(children) == 2:
            return (children[0], children[1])
        if len(children) == 1:
            child = children[0]
            return (child, None) if child.item < base.item else (None, child)
        return (None, None)

    @staticmethod
    def get(base: Node[C], item: C) -> Node[C]:
        if base.item == item:
            return base

        left, right = _BinaryTreeHandler.left_right(base)
        if left and item < base.item:
            return _BinaryTreeHandler.get(left, item)
        elif right and item >= base.item:
            return _BinaryTreeHandler.get(right, item)
        else:
            raise ValueError(f"No such item in tree: {item}")

    @staticmethod
    def add(base: Node[C], node: Node[C]) -> None:
        left, right = _BinaryTreeHandler.left_right(base)
        if left and node.item < base.item:
            _BinaryTreeHandler.add(left, node)
        elif right and node.item >= base.item:
            _BinaryTreeHandler.add(right, node)
        else:
            base.add_children(node)

    @staticmethod
    def unlink(base: Node[C]) -> Tuple[Optional[Node[C]], Sequence[Node[C]]]:
        parent = base.parents[0] if base.parents else None
        children = tuple(
            c for c in _BinaryTreeHandler.left_right(base) if c is not None
        )
        base.remove_parents(*base.parents)
        base.remove_children(*base.children)
        return parent, children


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
            left, right = _BinaryTreeHandler.left_right(node)
            left_height = get_height(left) if left else 0
            right_height = get_height(right) if right else 0
            return 1 + max(left_height, right_height)

        return get_height(self.root) if self.root else 0

    @property
    def mappings(self) -> List[NodeMap[C]]:
        def get_mappings(node: Node[C]) -> List[NodeMap[C]]:
            left, right = _BinaryTreeHandler.left_right(node)
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
        _BinaryTreeHandler.add(self.root, item_node)

    def remove(self, item: C) -> None:
        if not self.root:
            raise ValueError(f"No such item in tree: {item}")

        node = _BinaryTreeHandler.get(self.root, item)
        parent, children = _BinaryTreeHandler.unlink(node)
        if self.root == node:
            self.__assign_root(children)
        elif parent:
            for child in children:
                _BinaryTreeHandler.add(parent, child)
        else:
            raise ValueError

    def __assign_root(self, children: Sequence[Node[C]]) -> None:
        self.__root = None
        for child in children:
            if self.root is None:
                self.__root = child
            else:
                _BinaryTreeHandler.add(self.root, child)
