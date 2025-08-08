import pytest
from pyalgo import node
from pyalgo.tree import binary_tree


class TestBinaryTree:
    @pytest.fixture
    def tree(self) -> binary_tree.BinaryTree:
        return binary_tree.BinaryTree()

    def test_root(self, tree: binary_tree.BinaryTree):
        assert tree.root == None
        tree.add(1)
        assert isinstance(tree.root, node.Node) and tree.root.item == 1

    def test_add(self, tree: binary_tree.BinaryTree):
        items = [1, 2, -4, -1, 1]
        for item in items:
            tree.add(item)
        assert isinstance(tree.root, node.Node) and tree.root.item == 1
        assert tree.root.parents == ()

        right, left = tree.root.children
        assert left.item == -4 and left.parents == (tree.root,)
        assert len(left.children) == 1 and left.children[0].item == -1

        assert right.item == 2 and right.parents == (tree.root,)
        assert len(right.children) == 1 and right.children[0].item == 1
