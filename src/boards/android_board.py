import dataclasses
from boards import board
from typing import List


@dataclasses.dataclass
class NodePositions:
    top_left: board.Node
    top_centre: board.Node
    top_right: board.Node
    mid_left: board.Node
    mid_centre: board.Node
    mid_right: board.Node
    bottom_left: board.Node
    bottom_centre: board.Node
    bottom_right: board.Node


class AndroidBoard(board.Board):
    def __init__(self, positions: "NodePositions"):
        self._positions = positions
        nodes = [getattr(positions, f.name) for f in dataclasses.fields(positions)]
        self._active_node = self._get_active(nodes)

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
