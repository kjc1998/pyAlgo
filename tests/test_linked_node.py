import pytest
from pyalgo import linked_node


class TestLinkedNode:
    @pytest.fixture
    def node(self) -> linked_node.LinkedNode[str]:
        node = linked_node.LinkedNode("root")
        return node

    def test_properties(self, node: linked_node.LinkedNode[str]) -> None:
        assert node.element == "root"
        assert node.parent == None
        assert node.children == []
        assert node == linked_node.LinkedNode("root")

    def test_set_parent(self, node: linked_node.LinkedNode[str]) -> None:
        assert node.parent == None
        parent = linked_node.LinkedNode("cde")
        node.set_parent(parent)
        assert node.parent == parent
        assert parent.children == [node]

    def test_add_children(self, node: linked_node.LinkedNode[str]) -> None:
        assert node.children == []
        one = linked_node.LinkedNode("bcd")
        two = linked_node.LinkedNode("cde")
        three = linked_node.LinkedNode("def")

        node.add_children(one, two)
        node.add_children(one)  # will not be added again
        node.add_children(three)
        assert node.children == [one, two, three]
        assert one.parent == two.parent == three.parent == node

    def test_remove_parent(self, node: linked_node.LinkedNode[str]) -> None:
        one = linked_node.LinkedNode("bcd")
        two = linked_node.LinkedNode("cde")
        one.set_parent(node)
        two.set_parent(node)
        assert one.parent == two.parent == node
        assert node.children == [one, two]
        one.remove_parent()
        assert one.parent == None
        assert node.children == [two]

    def test_remove_children(self, node: linked_node.LinkedNode[str]) -> None:
        one = linked_node.LinkedNode("bcd")
        two = linked_node.LinkedNode("cde")
        node.add_children(one, two)
        assert one.parent == two.parent == node
        assert node.children == [one, two]
        node.remove_children(one)
        assert one.parent == None
        assert node.children == [two]

    def test_unlink(self, node: linked_node.LinkedNode[str]) -> None:
        node = linked_node.LinkedNode("root")
        one = linked_node.LinkedNode("1")
        two = linked_node.LinkedNode("2")
        node.add_children(one)
        one.add_children(two)
        assert node.parent == None
        assert one.parent == node
        assert two.parent == one
        one.unlink()
        assert node.children == [two]
        assert two.parent == node
        assert one.parent == None and one.children == []

    def test_unlink_none(self, node: linked_node.LinkedNode[str]) -> None:
        node = linked_node.LinkedNode("root")
        one = linked_node.LinkedNode("1")
        two = linked_node.LinkedNode("2")
        node.add_children(one)
        two.set_parent(one)
        assert one.parent == node and two.parent == one
        node.unlink()
        assert node.parent == None and node.children == []
        assert one.parent == None and one.children == [two]
