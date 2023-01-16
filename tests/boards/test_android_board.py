import pytest
from boards import board, android_board


class TestAndroidBoard:
    @pytest.fixture
    def linked_nodes(self):
        node_one = board.Node("1", visited=True)
        node_two = board.Node("2", visited=True, parent=node_one)
        node_three = board.Node("3", visited=True, parent=node_two)
        node_active = board.Node("4", active=True, visited=True, parent=node_three)
        return [node_one, node_two, node_three, node_active]

    @pytest.fixture
    def board_model(self, linked_nodes):
        other_nodes = [board.Node(str(i)) for i in range(5, 10)]
        positions = android_board.NodePositions(*linked_nodes, *other_nodes)
        return android_board.AndroidBoard(positions)

    def test_get_sequence(self, linked_nodes, board_model):
        expected = linked_nodes
        observed = board_model.get_sequence()
        assert expected == observed
