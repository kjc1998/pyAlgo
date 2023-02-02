import pytest
import dataclasses
from boards import board as board_, android_board, coordinates


class TestNodePositionController:
    def test_read_only_access(self):
        controller = android_board.NodePositionController()
        with pytest.raises(dataclasses.FrozenInstanceError):
            controller.top_centre = 1

    def test_activate(self):
        controller = android_board.NodePositionController()
        node_one = controller.top_centre
        node_two = controller.bottom_right

        controller.activate(node_one)
        assert node_one.active and node_one.visited and node_one.parent is None

        controller.activate(node_two)
        assert not node_one.active and node_one.visited
        assert node_two.active and node_two.visited and node_two.parent == node_one

    def test_get_node_by_id(self):
        node_one = board_.Node("1")
        controller = android_board.NodePositionController(node_one)
        observed = controller.get_node_by_id("1")
        assert node_one == observed
        with pytest.raises(KeyError):
            controller.get_node_by_id("10")

    def test_string(self):
        controller = android_board.NodePositionController()
        expected = "0\t0\t0\n0\t0\t0\n0\t0\t0\n"
        observed = str(controller)
        assert expected == observed

    def test_same_id_error(self):
        with pytest.raises(ValueError):
            android_board.NodePositionController(
                board_.Node("2"),
                board_.Node("2"),
            )

    def test_active_node_error(self):
        controller = android_board.NodePositionController()
        with pytest.raises(ValueError):
            controller.get_active_node()


class TestAndroidMapper:
    def build_two_index(self, value):
        if isinstance(value, tuple):
            return coordinates.TwoIndex(*value)
        if isinstance(value, list):
            return [coordinates.TwoIndex(*v) for v in value]
        if isinstance(value, set):
            return {coordinates.TwoIndex(*v) for v in value}

    def test_get_perimeters(self):
        mapper = android_board.AndroidMapper(3, 3)
        expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
        observed = list(mapper._get_perimeters())
        assert self.build_two_index(expected) == observed

    @pytest.mark.parametrize(
        "index, expected",
        [
            pytest.param(
                (0, 0), {(0, 1), (1, 0), (1, 2), (2, 1), (1, 1)}, id="corner_case"
            ),
            pytest.param(
                (1, 1),
                {(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)},
                id="middle_case",
            ),
            pytest.param(
                (0, 2),
                {(1, 0), (0, -1), (1, -1), (1, -2), (2, -1)},
                id="adjacent_corner_case",
            ),
            pytest.param(
                (0, 1),
                {(0, -1), (1, -1), (2, -1), (1, 0), (2, 1), (1, 1), (0, 1)},
                id="edge_case",
            ),
        ],
    )
    def test_get_gradient_lines(self, index, expected):
        mapper = android_board.AndroidMapper(3, 3)
        observed = mapper._get_gradient_lines(self.build_two_index(index))
        assert self.build_two_index(expected) == observed

    @pytest.mark.parametrize(
        "index, gradient, expected",
        [
            pytest.param((0, 0), (1, 1), [(1, 1), (2, 2)], id="diagonal_case"),
            pytest.param((0, 0), (1, 2), [(1, 2)], id="straight_across"),
            pytest.param((2, 2), (-1, 0), [(1, 2), (0, 2)], id="straight_down"),
        ],
    )
    def test_get_line_indices(self, index, gradient, expected):
        mapper = android_board.AndroidMapper(3, 3)
        observed = mapper._get_line_indices(index, gradient)
        assert expected == observed

    @pytest.mark.parametrize(
        "row, column, expected",
        [
            # fmt: off
            pytest.param(
                3, 3, {
                    (0, 0): [[(0, 1), (0, 2)], [(1, 2)], [(2, 1)], [(1, 1), (2, 2)], [(1, 0), (2, 0)]],
                    (0, 1): [[(0, 2)], [(2, 0)], [(2, 2)], [(1, 2)], [(1, 0)], [(1, 1), (2, 1)], [(0, 0)]],
                    (0, 2): [[(2, 1)], [(1, 1), (2, 0)], [(1, 0)], [(1, 2), (2, 2)], [(0, 1), (0, 0)]],
                    (1, 0): [[(1, 1), (1, 2)], [(2, 2)], [(0, 1)], [(2, 1)], [(0, 0)], [(2, 0)], [(0, 2)]],
                    (1, 1): [[(1, 2)], [(0, 0)], [(0, 2)], [(2, 2)], [(2, 0)], [(0, 1)], [(2, 1)], [(1, 0)]],
                    (1, 2): [[(0, 1)], [(0, 0)], [(2, 0)], [(2, 1)], [(0, 2)], [(2, 2)], [(1, 1), (1, 0)]],
                    (2, 0): [[(2, 1), (2, 2)], [(0, 1)], [(1, 1), (0, 2)], [(1, 0), (0, 0)], [(1, 2)]],
                    (2, 1): [[(2, 2)], [(1, 0)], [(0, 0)], [(0, 2)], [(1, 2)], [(1, 1), (0, 1)], [(2, 0)]],
                    (2, 2): [[(1, 0)], [(0, 1)], [(1, 1), (0, 0)], [(1, 2), (0, 2)], [(2, 1), (2, 0)]],
                },
                id="3-by-3_test"
            ),
            pytest.param(
                2, 3, {
                    (0, 0): [[(0, 1), (0, 2)], [(1, 0)], [(1, 1)], [(1, 2)]],
                    (0, 1): [[(0, 2)], [(1, 2)], [(1, 0)], [(1, 1)], [(0, 0)]],
                    (0, 2): [[(1, 2)], [(1, 1)], [(0, 1), (0, 0)], [(1, 0)]],
                    (1, 0): [[(0, 0)], [(0, 1)], [(0, 2)], [(1, 1), (1, 2)]],
                    (1, 1): [[(1, 2)], [(0, 0)], [(0, 2)], [(0, 1)], [(1, 0)]],
                    (1, 2): [[(0, 2)], [(0, 1)], [(1, 1), (1, 0)], [(0, 0)]],
                },
                id="2-by-3_test",
            )
            # fmt: on
        ],
    )
    def test_map(self, row, column, expected):
        mapper = android_board.AndroidMapper(row, column)
        observed = mapper.map
        assert expected == observed

    def test_get_paths(self):
        mapper = android_board.AndroidMapper(3, 3)
        expected = [
            [(0, 1), (0, 2)],
            [(1, 2)],
            [(2, 1)],
            [(1, 1), (2, 2)],
            [(1, 0), (2, 0)],
        ]
        observed = mapper.get_paths((0, 0))
        assert expected == observed


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
        controller = android_board.NodePositionController(*linked_nodes, *other_nodes)
        return android_board.AndroidBoard(controller)

    def test_eq(self):
        controller = android_board.NodePositionController()
        board_one = android_board.AndroidBoard(controller)
        board_two = android_board.AndroidBoard(controller)
        assert board_one == board_two

    def test_str(self):
        controller = android_board.NodePositionController()
        board = android_board.AndroidBoard(controller)
        expected = "AndroidBoard(\n0\t0\t0\n0\t0\t0\n0\t0\t0\n)"
        observed = str(board)
        assert expected == observed

    def test_get_sequence(self, linked_nodes, board_model):
        expected = linked_nodes
        observed = board_model.get_sequence()
        assert expected == observed

    def test_get_next_boards(self):
        start_node = board_.Node("mid_left", True, True)
        controller = android_board.NodePositionController(mid_left=start_node)
        board = android_board.AndroidBoard(controller)
        mapper = android_board.AndroidMapper(3, 3)
        expected_controllers = [
            android_board.NodePositionController(
                top_left=board_.Node("1", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                top_centre=board_.Node("2", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                top_right=board_.Node("3", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                mid_centre=board_.Node("5", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                bottom_left=board_.Node("7", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                bottom_centre=board_.Node("8", True, True, start_node),
                mid_left=start_node,
            ),
            android_board.NodePositionController(
                bottom_right=board_.Node("9", True, True, start_node),
                mid_left=start_node,
            ),
        ]

        expected = [android_board.AndroidBoard(c) for c in expected_controllers]
        observed = board.get_next_boards(mapper)
        assert not start_node.active and start_node.visited
        assert len(expected) == len(observed) and [x in observed for x in expected]
