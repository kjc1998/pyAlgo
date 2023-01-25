import pytest
from boards import board as board_, android_board


def test_same_id_error():
    with pytest.raises(ValueError):
        android_board.NodePositions(
            board_.Node("2"),
            board_.Node("2"),
        )


class TestAndroidBoard:
    @pytest.fixture
    def linked_nodes(self):
        node_one = board_.Node("1", visited=True)
        node_two = board_.Node("2", visited=True, parent=node_one)
        node_three = board_.Node("3", visited=True, parent=node_two)
        node_active = board_.Node("4", active=True, visited=True, parent=node_three)
        return [node_one, node_two, node_three, node_active]

    @pytest.fixture
    def board_model(self, linked_nodes):
        other_nodes = [board_.Node(str(i)) for i in range(5, 10)]
        positions = android_board.NodePositions(*linked_nodes, *other_nodes)
        return android_board.AndroidBoard(positions)

    def test_repr(self, capsys):
        positions = android_board.NodePositions(
            board_.Node("1", visited=True),
            board_.Node("2", visited=True, active=True),
        )
        board = android_board.AndroidBoard(positions)
        print(board)
        expected = "AndroidBoard(\n1\tX\t0\n0\t0\t0\n0\t0\t0\n)\n"
        observed = capsys.readouterr().out
        assert observed == expected

    def test_eq(self):
        positions = android_board.NodePositions()
        board_one = android_board.AndroidBoard(positions)
        board_two = android_board.AndroidBoard(positions)
        assert board_one == board_two

    def test_get_sequence(self, linked_nodes, board_model):
        expected = linked_nodes
        observed = board_model.get_sequence()
        assert expected == observed
