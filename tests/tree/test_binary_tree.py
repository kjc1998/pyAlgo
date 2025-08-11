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

    def test_height(self, tree: binary_tree.BinaryTree):
        assert tree.height == 0
        tree.add(1)
        assert tree.height == 1
        items = [2, 4, 6, -1, 0, -2, -5]
        for item in items:
            tree.add(item)
        assert tree.height == 4

    def test_add(self, tree: binary_tree.BinaryTree):
        items = [1, 2, -4, -1, 1]
        for item in items:
            tree.add(item)
        assert isinstance(tree.root, node.Node) and tree.root.item == 1
        assert tree.mappings == [(1, [-4, 2]), (-4, [-1]), (-1, []), (2, [1]), (1, [])]

    def test_root_remove(self, tree: binary_tree.BinaryTree):
        with pytest.raises(ValueError):
            tree.remove(1)
        tree.add(1)
        assert tree.root and tree.root.item == 1
        tree.remove(1)
        assert tree.root == None

    def test_complex_remove(self, tree: binary_tree.BinaryTree):
        items = [1, 2, -1, 4, 1]
        for item in items:
            tree.add(item)
        assert tree.root and tree.root.item == 1
        assert tree.mappings == [(1, [-1, 2]), (-1, []), (2, [1, 4]), (1, []), (4, [])]
        tree.remove(2)
        assert tree.mappings == [(1, [-1, 1]), (-1, []), (1, [4]), (4, [])]

    def test_complex_root_remove(self, tree: binary_tree.BinaryTree):
        items = [1, 2, -1, 4, 1]
        for item in items:
            tree.add(item)
        assert tree.mappings == [(1, [-1, 2]), (-1, []), (2, [1, 4]), (1, []), (4, [])]
        tree.remove(1)
        assert tree.mappings == [(-1, [2]), (2, [1, 4]), (1, []), (4, [])]

    def test_remove_error(self, tree: binary_tree.BinaryTree):
        items = [1, 2, -1, 4, 1]
        for item in items:
            tree.add(item)
        tree.remove(1)
        tree.remove(1)
        with pytest.raises(ValueError):
            tree.remove(1)
