import dataclasses
import textwrap
import math
from boards import board
from typing import Any, Dict, Iterable, NewType, List, Set, Tuple

Coordinate = NewType("Coordinate", Tuple[int, int])


@dataclasses.dataclass(frozen=True)
class NodePositionController:
    # fmt: off
    top_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("1"))
    top_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("2"))
    top_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("3"))
    mid_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("4"))
    mid_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("5"))
    mid_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("6"))
    bottom_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("7"))
    bottom_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("8"))
    bottom_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("9"))
    # fmt: on

    def __iter__(self) -> Iterable[board.Node]:
        field_names = [field.name for field in dataclasses.fields(self)]
        for field_name in field_names:
            yield getattr(self, field_name)

    def __str__(self) -> str:
        content = f"""\
        {self.top_left}\t{self.top_centre}\t{self.top_right}
        {self.mid_left}\t{self.mid_centre}\t{self.mid_right}
        {self.bottom_left}\t{self.bottom_centre}\t{self.bottom_right}
        """
        return textwrap.dedent(content)

    def get_node_by_id(self, uid: str) -> board.Node:
        for node in self:
            if node.id == uid:
                return node
        raise KeyError(f"no such node with id: {uid}")

    def activate(self, active_node: board.Node) -> None:
        for node in self:
            if node.id == active_node.id:
                node.active = True
                node.visited = True
            else:
                node.activate = False

    def __post_init__(self):
        checked_list = []
        for node in self:
            if node.id in checked_list:
                raise ValueError(f"id: {node.id} has already been used")
            checked_list.append(node.id)


class AndroidMapper:
    def __init__(self, row: int, column: int):
        self._indices = [(i, j) for i in range(row) for j in range(column)]

    def get_path_map(self) -> Dict["Coordinate", List[List["Coordinate"]]]:
        result = {}
        for index in self._indices:
            gradients = self._get_gradient_lines(index)
            result[index] = [self._get_line_indices(index, g) for g in gradients]
        return result

    def _get_line_indices(
        self, index: "Coordinate", gradient: "Coordinate"
    ) -> List["Coordinate"]:
        result = []
        mutiplier = 1
        while True:
            next_x = index[0] + mutiplier * gradient[0]
            next_y = index[1] + mutiplier * gradient[1]
            if (next_x, next_y) in self._indices:
                result.append((next_x, next_y))
                mutiplier += 1
            else:
                break
        return result

    def _get_gradient_lines(self, index: "Coordinate") -> Set["Coordinate"]:
        result = set()
        for end_index in self._perimeters:
            if index == end_index:
                continue
            diff_x = end_index[0] - index[0]
            diff_y = end_index[1] - index[1]
            common_divisor = math.gcd(diff_x, diff_y)
            gradient = (int(diff_x / common_divisor), int(diff_y / common_divisor))
            result.add(gradient)
        return result

    @property
    def _perimeters(self) -> List["Coordinate"]:
        result = []
        range_x = range(max(self._indices)[0] + 1)
        range_y = range(max(self._indices)[1] + 1)

        for i, index in enumerate(self._indices):
            x, y = i // 3, i % 3
            check_x = x - 1 in range_x and x + 1 in range_x
            check_y = y - 1 in range_y and y + 1 in range_y
            if not (check_x and check_y):
                result.append(index)
        return result


class AndroidBoard(board.Board):
    def __init__(self, controller: "NodePositionController"):
        self._controller = controller

    def __str__(self) -> str:
        return f"{type(self).__name__}(\n{str(self._controller)})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self._controller == other._controller

    def get_sequence(self) -> List[board.Node]:
        result = [self._get_active_node()]
        current = result[0]
        while current.parent:
            current = current.parent
            result.insert(0, current)
        return result

    def get_next_boards(self) -> List[board.Board]:
        raise NotImplementedError

    def _get_active_node(self) -> board.Node:
        for node in self._controller:
            if node.active:
                return node
        raise ValueError("no active node")
