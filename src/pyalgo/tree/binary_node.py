from pyalgo import linked_node
from pyalgo.models import WeightedElement, Numbers
from typing import Optional


class BinaryNode(linked_node.LinkedNode[WeightedElement]):
    def __init__(self, element: WeightedElement) -> None:
        super().__init__(element)

    @property
    def left(self) -> Optional[linked_node.LinkedNode[WeightedElement]]:
        for child in self.children:
            if self.__is_left_weight(child.element.weight):
                return child
        return None

    @property
    def right(self) -> Optional[linked_node.LinkedNode[WeightedElement]]:
        for child in self.children:
            if not self.__is_left_weight(child.element.weight):
                return child
        return None

    def get(self, weight: Numbers) -> "BinaryNode[WeightedElement]":
        if weight == self.element.weight:
            return self
        elif self.__is_left_weight(weight) and isinstance(self.left, BinaryNode):
            return self.left.get(weight)
        elif not self.__is_left_weight(weight) and isinstance(self.right, BinaryNode):
            return self.right.get(weight)
        raise ValueError(f"no such element of weight: {weight}")

    def add_children(self, *children: linked_node.LinkedNode[WeightedElement]) -> None:
        for child in children:
            if self.left and self.__is_left_weight(child.element.weight):
                self.left.add_children(child)
            elif self.right and not self.__is_left_weight(child.element.weight):
                self.right.add_children(child)
            else:
                super().add_children(child)

    def __is_left_weight(self, weight: Numbers) -> bool:
        return weight <= self.element.weight
