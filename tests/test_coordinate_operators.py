import pytest

import coordinates, coordinate_operators


def build_coordinate_2d(tuples):
    return [coordinates.Coordinate2D(*x) for x in tuples]


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param([(1, 1)], [(1, 1)], id="unit_case"),
        pytest.param(
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            id="box_case",
        ),
        pytest.param(
            # fmt: off
            [
                (0, 0), (0, 1),
                (1, 0), (1, 1),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                (5, 3), (5, 4),
            ],
            [
                (0, 0), (0, 1),
                (1, 0), (1, 1),
                (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                (3, 0), (3, 4),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                (5, 3), (5, 4),
            ],
            # fmt: on
            id="corner_case",
        ),
    ],
)
def test_get_edge_coordinates(input, expected):
    observed = coordinate_operators.get_edge_coordinates(build_coordinate_2d(input))
    expected_coords = build_coordinate_2d(expected)
    assert len(expected_coords) == len(observed)
    for coord in observed:
        assert coord in expected_coords


@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param(((2, 3), (5, 7)), (3, 4), id="standard_test"),
        pytest.param(((2, 0), (4, 0)), (1, 0), id="factorised_test"),
        pytest.param(((4, 0), (2, 0)), (-1, 0), id="negative_test"),
    ],
)
def test_get_gradient(input, expected):
    coord_one = coordinates.Coordinate2D(*input[0])
    coord_two = coordinates.Coordinate2D(*input[1])
    expected = coordinates.Coordinate2D(*expected)
    observed = coordinate_operators.get_unit_gradient(coord_one, coord_two)
    assert expected == observed


@pytest.mark.parametrize(
    "start_coord, end_coord, unit_gradient, expected",
    [
        pytest.param((0, 0), (2, 2), (1, 1), [(1, 1), (2, 2)], id="diagonal_test"),
        pytest.param((0, 0), (-5, 0), (-1, 0), [], id="out_of_bounds_test"),
    ],
)
def test_get_line_coordinates(start_coord, end_coord, unit_gradient, expected):
    coord_pool = [
        coordinates.Coordinate2D(0, 0),
        coordinates.Coordinate2D(0, 1),
        coordinates.Coordinate2D(0, 2),
        coordinates.Coordinate2D(1, 0),
        coordinates.Coordinate2D(1, 1),
        coordinates.Coordinate2D(1, 2),
        coordinates.Coordinate2D(2, 0),
        coordinates.Coordinate2D(2, 1),
        coordinates.Coordinate2D(2, 2),
    ]
    observed_end = coordinate_operators.get_line_coordinates(
        coord_pool,
        coordinates.Coordinate2D(*start_coord),
        end_coord=coordinates.Coordinate2D(*end_coord),
    )
    observed_gradient = coordinate_operators.get_line_coordinates(
        coord_pool,
        coordinates.Coordinate2D(*start_coord),
        unit_gradient=coordinates.Coordinate2D(*unit_gradient),
    )
    assert build_coordinate_2d(expected) == observed_end == observed_gradient
