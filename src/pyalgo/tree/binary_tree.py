from pyalgo import linked_node
from pyalgo.tree import tree, binary_node
from pyalgo.models import Numbers, WeightedElement
from typing import Dict, List, Optional


class BinaryTree(tree.Tree[WeightedElement]):
    def __init__(self, *elements: WeightedElement) -> None:
        self.__uids = set[str]()
        self.__node: Optional[binary_node.BinaryNode[WeightedElement]] = None
        for element in elements:
            self.insert(element)

    def get(self, weight: Numbers) -> WeightedElement:
        return self.__get_node(weight).element

    def insert(self, element: WeightedElement) -> None:
        if element.uid in self.__uids:
            raise ValueError(f"element of uid: {element.uid} already exists")
        self.__uids.add(element.uid)
        if self.__node is None:
            self.__node = binary_node.BinaryNode(element)
        else:
            self.__node.add_children(binary_node.BinaryNode(element))

    def delete(self, weight: Numbers) -> None:
        node = self.__get_node(weight)
        # if node is self.__node:
        #     left, right = self.__node.left, self.__node.right
        #     node.unlink()
        # else:
        #     node.unlink()

    def get_mapping(self) -> Dict[WeightedElement, List[WeightedElement]]:
        def get_node_mapping(
            node: linked_node.LinkedNode[WeightedElement],
        ) -> Dict[WeightedElement, List[WeightedElement]]:
            left_map, right_map = {}, {}
            if isinstance(node, binary_node.BinaryNode):
                left_map = get_node_mapping(node.left) if node.left else {}
                right_map = get_node_mapping(node.right) if node.right else {}
            children_elements = [i.element for i in node.children]
            return {node.element: children_elements, **left_map, **right_map}

        return get_node_mapping(self.__node) if self.__node else {}

    def __get_node(self, weight: Numbers) -> binary_node.BinaryNode[WeightedElement]:
        if self.__node:
            return self.__node.get(weight)
        raise ValueError(f"no such element of weight: {weight}")
