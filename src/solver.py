from typing import Dict, List
from boards import board as board_


class Solver:
    @staticmethod
    def solve(board: board_.Board) -> Dict[int, List[board_.Node]]:
        next_boards = board.get_next_boards()
        if len(next_boards) > 0:
            sequences = [Solver.solve(b) for b in next_boards]
            result = {k: v for sequence in sequences for k, v in sequence.items()}
            return result
        return {board.uid: board.get_sequence()}
