import dataclasses
import textwrap
import math
import copy

from boards import board, coordinates
from typing import Any, Dict, Iterable, List, Set


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

    def get_active_node(self) -> board.Node:
        for node in self:
            if node.active:
                return node
        raise ValueError("no active node")

    def get_node_by_id(self, uid: str) -> board.Node:
        for node in self:
            if node.id == uid:
                return node
        raise KeyError(f"no such node with id: {uid}")

    def activate(self, activate: board.Node) -> None:
        try:
            active_node = self.get_active_node()
            active_node.active = False
        except ValueError:
            active_node = None
        for node in self:
            if node.id == activate.id:
                node.active = True
                node.visited = True
                node.parent = active_node

    def __post_init__(self):
        checked_list = []
        for node in self:
            if node.id in checked_list:
                raise ValueError(f"id: {node.id} has already been used")
            checked_list.append(node.id)


class AndroidMapper:
    def __init__(self, row: int, column: int):
        self._coordinates = [
            coordinates.TwoIndex(i, j) for i in range(row) for j in range(column)
        ]

    @property
    def map(
        self,
    ) -> Dict[coordinates.TwoIndex, List[List[coordinates.TwoIndex]]]:
        if not hasattr(self, "_result"):
            self._result = {}
            for index in self._indices:
                gradients = self._get_gradient_lines(index)
                self._result[index] = [
                    self._get_line_indices(index, g) for g in gradients
                ]
        return self._result

    def get_paths(
        self, index: coordinates.TwoIndex
    ) -> List[List[coordinates.TwoIndex]]:
        map = self.map
        return map[index]

    def _get_line_indices(
        self,
        index: coordinates.TwoIndex,
        gradient: coordinates.TwoIndex,
    ) -> List[coordinates.TwoIndex]:
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

    def _get_gradient_lines(
        self, coord: coordinates.TwoIndex
    ) -> Set[coordinates.TwoIndex]:
        result = set()
        for edge in list(self._get_perimeters()):
            if coord == edge:
                continue
            diff = edge - coord
            divisor = math.gcd(diff.x, diff.y)
            gradient = coordinates.TwoIndex(
                int(diff.x / divisor), int(diff.y / divisor)
            )
            result.add(gradient)
        return result

    def _get_perimeters(self) -> List[coordinates.TwoIndex]:
        range_x = range(max(self._coordinates).x + 1)
        range_y = range(max(self._coordinates).y + 1)

        for i, coordinate in enumerate(self._coordinates):
            x, y = i // 3, i % 3
            check_x = x - 1 in range_x and x + 1 in range_x
            check_y = y - 1 in range_y and y + 1 in range_y
            if not (check_x and check_y):
                yield coordinate


class IndexMapper:
    def __init__(self, uids: List[str], nodes: List[board.Node]):
        self._uid_coordinate = {uid: (i // 3, i % 3) for i, uid in enumerate(uids)}
        self._coordinate_node = dict(zip(self._uid_coordinate.values(), nodes))

    def get_coordinate(self, node: board.Node) -> coordinates.TwoIndex:
        return self._uid_coordinate[node.id]

    def get_node(self, coordinate: coordinates.TwoIndex) -> board.Node:
        return self._coordinate_node[coordinate]


class AndroidBoard(board.Board):
    def __init__(self, controller: "NodePositionController"):
        self._controller = controller
        self._node_map = {node.id: node for node in controller}
        self._index_map = IndexMapper(self._node_map.keys(), self._node_map.values())

    def __str__(self) -> str:
        return f"{type(self).__name__}(\n{str(self._controller)})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self._controller == other._controller

    def get_sequence(self) -> List[board.Node]:
        result = [self._controller.get_active_node()]
        current = result[0]
        while current.parent:
            current = current.parent
            result.insert(0, current)
        return result

    def get_next_boards(self, mapper: AndroidMapper) -> List[board.Board]:
        active_node = self._controller.get_active_node()
        active_index = self._index_map.get_coordinate(active_node)
        paths = mapper.get_paths(active_index)
        next_nodes = self._get_next_nodes(paths)
        result = []
        for next_node in next_nodes:
            controller = copy.copy(self._controller)
            controller.activate(next_node)
            result.append(AndroidBoard(controller))
        return result

    def _get_next_nodes(
        self, paths: List[List[coordinates.TwoIndex]]
    ) -> List[board.Node]:
        result = []
        for path in paths:
            for coordinate in path:
                node = self._index_map.get_node(coordinate)
                if not node.visited:
                    result.append(node)
                    break
        return result
