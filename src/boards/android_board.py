from boards import board
from typing import List


class AndroidBoard(board.Board):
    def __init__(self, nodes: List[board.Node]):
        self._nodes = nodes
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
