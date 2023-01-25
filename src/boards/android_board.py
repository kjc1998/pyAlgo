import dataclasses
import textwrap
from boards import board
from typing import Any, List


@dataclasses.dataclass
class NodePositions:
    top_left: board.Node = board.Node("1")
    top_centre: board.Node = board.Node("2")
    top_right: board.Node = board.Node("3")
    mid_left: board.Node = board.Node("4")
    mid_centre: board.Node = board.Node("5")
    mid_right: board.Node = board.Node("6")
    bottom_left: board.Node = board.Node("7")
    bottom_centre: board.Node = board.Node("8")
    bottom_right: board.Node = board.Node("9")

    def __post_init__(self):
        field_names = [field.name for field in dataclasses.fields(self)]
        checked_list = []
        for field_name in field_names:
            node = getattr(self, field_name)
            if node.id in checked_list:
                raise ValueError(f"id: {node.id} has already been used")
            checked_list.append(node.id)


class AndroidBoard(board.Board):
    def __init__(self, positions: "NodePositions"):
        self._positions = positions
        nodes = [getattr(positions, f.name) for f in dataclasses.fields(positions)]
        self._active_node = self._get_active(nodes)

    def __repr__(self) -> str:
        def repr(node: board.Node) -> str:
            if node.active:
                return "X"
            if node.visited:
                return "1"
            return "0"

        pos = self._positions
        content = f"""\
        {type(self).__name__}(
        {repr(pos.top_left)}\t{repr(pos.top_centre)}\t{repr(pos.top_right)}
        {repr(pos.mid_left)}\t{repr(pos.mid_centre)}\t{repr(pos.mid_right)}
        {repr(pos.bottom_left)}\t{repr(pos.bottom_centre)}\t{repr(pos.bottom_right)}
        )"""
        return textwrap.dedent(content)

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) == type(other)
            and self._positions == other._positions
            and self._active_node == other._active_node
        )

    def get_sequence(self) -> List[board.Node]:
        result = [self._active_node]
        current = self._active_node
        while current.parent:
            current = current.parent
            result.insert(0, current)
        return result

    def get_next_boards(self) -> List[board.Board]:
        raise NotImplementedError

    def _get_active(self, nodes: List[board.Node]) -> board.Node:
        for node in nodes:
            if node.active:
                return node
