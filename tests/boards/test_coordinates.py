import pytest
import coordinates


class TestPositiveCoordinate:
    def test_min_max(self):
        coord_one = coordinates.Coordinate2D(1, 2)
        coord_two = coordinates.Coordinate2D(2, 2)
        assert coord_two > coord_one
        assert min([coord_one, coord_two]) == coord_one
        assert max([coord_one, coord_two]) == coord_two

    def test_error_raised(self):
        with pytest.raises(ValueError):
            coordinates.Coordinate2D("test", 2)

    def test_add_subtraction(self):
        coord_one = coordinates.Coordinate2D(3, 4)
        coord_two = coordinates.Coordinate2D(1, 1)
        assert coord_one + coord_two == coordinates.Coordinate2D(4, 5)
        assert coord_one - coord_two == coordinates.Coordinate2D(2, 3)

    def test_multiplication(self):
        coord_one = coordinates.Coordinate2D(3, 4)
        expected = coordinates.Coordinate2D(9, 12)
        observed = coord_one * 3
        assert expected == observed
