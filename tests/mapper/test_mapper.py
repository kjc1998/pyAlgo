import pytest
from mapper import mapper


class TestNode:
    @pytest.fixture
    def node(self):
        return mapper.Node("123")

    def test_properties(self, node):
        assert node.uid == "123"
        assert node.active == False
        assert node.visited == False
        assert node.parent == None

    def test_set_unset_active(self, node):
        node.set_active()
        assert node.active == node.visited == True
        with pytest.raises(ValueError):
            node.set_active()
        node.unset_active()
        assert node.active == False
        assert node.visited == True
        with pytest.raises(ValueError):
            node.set_active()

    def test_set_parent(self, node):
        p_node = mapper.Node("parent")
        node.set_active(p_node)
        assert node.parent == p_node

    def test_str(self, node):
        assert str(node) == "0"
        node.set_active()
        assert str(node) == "X"
        node.unset_active()
        assert str(node) == "1"
