from pyalgo import linked_node
from pyalgo.tree import tree
from pyalgo.models import Numbers, WeightedElement
from typing import Dict, List, Optional

LinkedNode = linked_node.LinkedNode


class BinaryNode(LinkedNode[WeightedElement]):
    def __init__(self, element: WeightedElement) -> None:
        super().__init__(element)

    @property
    def left(self) -> Optional["LinkedNode[WeightedElement]"]:
        for child in self.children:
            if self.__is_left_weight(child.element.weight):
                return child
        return None

    @property
    def right(self) -> Optional["LinkedNode[WeightedElement]"]:
        for child in self.children:
            if not self.__is_left_weight(child.element.weight):
                return child
        return None

    def get(self, weight: Numbers) -> "LinkedNode[WeightedElement]":
        if weight == self.element.weight:
            return self
        elif self.__is_left_weight(weight) and isinstance(self.left, BinaryNode):
            return self.left.get(weight)
        elif not self.__is_left_weight(weight) and isinstance(self.right, BinaryNode):
            return self.right.get(weight)
        raise ValueError(f"no such element of weight: {weight}")

    def add_children(self, *children: LinkedNode[WeightedElement]) -> None:
        for child in children:
            if self.left and self.__is_left_weight(child.element.weight):
                self.left.add_children(child)
            elif self.right and not self.__is_left_weight(child.element.weight):
                self.right.add_children(child)
            else:
                super().add_children(child)

    def __is_left_weight(self, weight: Numbers) -> bool:
        return weight <= self.element.weight


class BinaryTree(tree.Tree[WeightedElement]):
    def __init__(self, *elements: WeightedElement) -> None:
        self.__uids = set[str]()
        self.__node: Optional["BinaryNode[WeightedElement]"] = None
        for element in elements:
            self.insert(element)

    def get(self, weight: Numbers) -> WeightedElement:
        if self.__node:
            return self.__node.get(weight).element
        raise ValueError(f"no such element of weight: {weight}")

    def insert(self, element: WeightedElement) -> None:
        if element.uid in self.__uids:
            raise ValueError(f"element of uid: {element.uid} already exists")
        self.__uids.add(element.uid)
        if self.__node is None:
            self.__node = BinaryNode(element)
        else:
            self.__node.add_children(BinaryNode(element))

    def delete(self, weight: Numbers) -> None:
        node = self.__node.get(weight)

    def get_mapping(self) -> Dict[WeightedElement, List[WeightedElement]]:
        def get_node_mapping(
            node: "LinkedNode[WeightedElement]",
        ) -> Dict[WeightedElement, List[WeightedElement]]:
            left_map, right_map = {}, {}
            if isinstance(node, BinaryNode):
                left_map = get_node_mapping(node.left) if node.left else {}
                right_map = get_node_mapping(node.right) if node.right else {}
            children_elements = [i.element for i in node.children]
            return {node.element: children_elements, **left_map, **right_map}

        return get_node_mapping(self.__node) if self.__node else {}
