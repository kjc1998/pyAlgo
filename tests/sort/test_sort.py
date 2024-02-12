import pytest
from pyalgo.sort import sort


@pytest.mark.parametrize(
    "func",
    [
        pytest.param(sort.quick_sort, id="quick_sort"),
        pytest.param(sort.merge_sort, id="merge_sort"),
    ],
)
@pytest.mark.parametrize(
    "input, expected",
    [
        pytest.param([], [], id="empty_case"),
        pytest.param([1], [1], id="single_number_case"),
        pytest.param([1, 4, 2, 6, 3, 7], [1, 2, 3, 4, 6, 7], id="standard_case"),
        pytest.param([1, 2, 2, 5, 5, 3, 3], [1, 2, 2, 3, 3, 5, 5], id="repeated_case"),
    ],
)
def test_sort(func, input, expected):
    observed = func(input)
    assert expected == observed
