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
        node_five = board.Node("5")
        return android_board.AndroidBoard([*linked_nodes, node_five])

    def test_get_sequence(self, linked_nodes, board_model):
        expected = linked_nodes
        observed = board_model.get_sequence()
        assert expected == observed
