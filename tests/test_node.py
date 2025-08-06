from pyalgo.tree import node


class TestNode:
    def test_repr(self):
        n1 = node.Node(1)
        assert repr(n1) == "Node(1)"

    def test_add(self):
        n1, n2, n3 = node.Node(1), node.Node(2), node.Node(3)
        n1.add_parents(n2)
        n1.add_children(n3)
        assert n1.parents == (n2,)
        assert n1.children == (n3,)

        assert n2.parents == ()
        assert n2.children == (n1,)

        assert n3.parents == (n1,)
        assert n3.children == ()

    def test_remove(self):
        n1, n2, n3 = node.Node(1), node.Node(2), node.Node(3)
        n1.add_parents(n2)
        n1.add_children(n3)
        assert n1.parents == (n2,)
        assert n2.children == (n1,)
        assert n1.children == (n3,)
        assert n3.parents == (n1,)

        n1.remove_parents(n2)
        assert n1.parents == n2.children == ()
        assert n1.children == (n3,)
        n1.remove_children(n3)
        assert n1.children == n3.parents == ()

    def test_complex(self):
        n1, n2, n3 = node.Node(1), node.Node(2), node.Node(3)
        n1.add_parents(n2, n3)
        assert n1.parents == (n2, n3)
        assert n2.parents == n3.parents == ()
        assert n2.children == n3.children == (n1,)
        n2.remove_children(n1)
        assert n1.parents == (n3,)
        assert n3.children == (n1,)
        assert n2.parents == n2.children == ()

    def test_properties(self):
        n1 = node.Node(1)
        assert n1.item == 1
