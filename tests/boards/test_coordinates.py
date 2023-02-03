import pytest
from boards import coordinates


class TestPositiveCoordinate:
    def test_min_max(self):
        coord_one = coordinates.TwoIndex(1, 2)
        coord_two = coordinates.TwoIndex(2, 2)
        assert coord_two > coord_one
        assert min([coord_one, coord_two]) == coord_one
        assert max([coord_one, coord_two]) == coord_two

    def test_error_raised(self):
        with pytest.raises(ValueError):
            coordinates.TwoIndex("test", 2)

    def test_add_subtraction(self):
        coord_one = coordinates.TwoIndex(3, 4)
        coord_two = coordinates.TwoIndex(1, 1)
        assert coord_one + coord_two == coordinates.TwoIndex(4, 5)
        assert coord_one - coord_two == coordinates.TwoIndex(2, 3)

    def test_multiplication(self):
        coord_one = coordinates.TwoIndex(3, 4)
        expected = coordinates.TwoIndex(9, 12)
        observed = coord_one * 3
        assert expected == observed
