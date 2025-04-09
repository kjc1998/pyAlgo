import pytest
import dataclasses
from pyalgo.tree import BinaryNode, BinaryTree
from typing import Dict, List


@dataclasses.dataclass(frozen=True)
class MockElement:
    uid: str
    weight: int


class TestBinaryNode:
    @pytest.fixture
    def node(self) -> BinaryNode["MockElement"]:
        element = MockElement("root", 0)
        return BinaryNode(element)

    def test_left_and_right(self, node: BinaryNode["MockElement"]) -> None:
        small = BinaryNode(MockElement("small", -1))
        big = BinaryNode(MockElement("small", 1))
        node.add_children(small, big)
        assert node.children == [small, big]
        assert small.children == big.children == []
        assert node.left == small
        assert node.right == big

    def test_add_children(self, node: BinaryNode["MockElement"]) -> None:
        one = BinaryNode(MockElement("abc", -2))
        two = BinaryNode(MockElement("bcd", -1))
        three = BinaryNode(MockElement("cde", 1))
        four = BinaryNode(MockElement("def", 2))
        node.add_children(one, two, three, four)
        assert node.children == [one, three]
        assert one.parent == three.parent == node
        assert one.children == [two] and three.children == [four]
        assert two.parent == one and four.parent == three

    def test_get(self, node: BinaryNode["MockElement"]) -> None:
        one = BinaryNode(MockElement("abc", -2))
        two = BinaryNode(MockElement("bcd", -1))
        three = BinaryNode(MockElement("cde", 1))
        four = BinaryNode(MockElement("def", 2))
        node.add_children(one, two, three, four)
        assert node.get(0) == node
        assert node.get(-1) == two


class TestBinaryTree:
    @pytest.fixture
    def tree(self) -> BinaryTree["MockElement"]:
        element = MockElement("root", 0)
        return BinaryTree(element)

    def test_get(self, tree: BinaryTree["MockElement"]) -> None:
        tree.insert(MockElement("a", 100))
        tree.insert(MockElement("b", 20))
        tree.insert(MockElement("c", -3))
        tree.insert(MockElement("d", 120))
        assert tree.get(120) == MockElement("d", 120)

    def test_get_error(self, tree: BinaryTree["MockElement"]) -> None:
        with pytest.raises(ValueError):
            tree.get(123)

    @pytest.mark.parametrize(
        "inserts, expected",
        [
            pytest.param(
                [],
                {MockElement("root", 0): []},
                id="root_case",
            ),
            pytest.param(
                [MockElement("left", -2), MockElement("right", 1)],
                {
                    MockElement("root", 0): [
                        MockElement("left", -2),
                        MockElement("right", 1),
                    ],
                    MockElement("left", -2): [],
                    MockElement("right", 1): [],
                },
                id="simple_case",
            ),
            pytest.param(
                [
                    MockElement("a", -2),
                    MockElement("b", 1),
                    MockElement("c", -7),
                    MockElement("d", -1),
                    MockElement("e", 1),
                    MockElement("f", 3),
                ],
                {
                    MockElement("root", 0): [
                        MockElement("a", -2),
                        MockElement("b", 1),
                    ],
                    MockElement("a", -2): [MockElement("c", -7), MockElement("d", -1)],
                    MockElement("b", 1): [MockElement("e", 1), MockElement("f", 3)],
                    MockElement("c", -7): [],
                    MockElement("d", -1): [],
                    MockElement("e", 1): [],
                    MockElement("f", 3): [],
                },
                id="complex_case_one",
            ),
            pytest.param(
                [
                    MockElement("c", -7),
                    MockElement("a", -2),
                    MockElement("d", -1),
                    MockElement("f", 3),
                    MockElement("b", 1),
                    MockElement("e", 1),
                ],
                {
                    # left
                    MockElement("root", 0): [
                        MockElement("c", -7),
                        MockElement("f", 3),
                    ],
                    MockElement("c", -7): [MockElement("a", -2)],
                    MockElement("a", -2): [MockElement("d", -1)],
                    MockElement("d", -1): [],
                    # right
                    MockElement("f", 3): [MockElement("b", 1)],
                    MockElement("b", 1): [MockElement("e", 1)],
                    MockElement("e", 1): [],
                },
                id="complex_case_two",
            ),
        ],
    )
    def test_insert(
        self,
        tree: BinaryTree["MockElement"],
        inserts: List["MockElement"],
        expected: Dict["MockElement", List["MockElement"]],
    ) -> None:
        for element in inserts:
            tree.insert(element)
        actual = tree.get_mapping()
        assert actual == expected

    def test_insert_duplicate_uid(self, tree: BinaryTree["MockElement"]) -> None:
        tree.insert(MockElement("abc", 100))
        tree.insert(MockElement("cde", 100))
        with pytest.raises(ValueError):
            tree.insert(MockElement("abc", 200))
        with pytest.raises(ValueError):
            tree.insert(MockElement("cde", 200))
