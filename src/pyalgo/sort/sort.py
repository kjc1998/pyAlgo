from typing import List
from pyalgo import models


def quick_sort(
    items: List[models.ComparableElement],
) -> List[models.ComparableElement]:
    if len(items) <= 1:
        return items
    pivot = items[-1]
    left, right = [], []
    for item in items[:-1]:
        if item < pivot:
            left.append(item)
        else:
            right.append(item)

    # can't do [*quick_sort(left), ...] because mypy has trouble recognising internal types
    return [i for i in quick_sort(left)] + [pivot] + [i for i in quick_sort(right)]


def merge_sort(
    items: List[models.ComparableElement],
) -> List[models.ComparableElement]:
    if len(items) <= 1:
        return items

    midpoint = len(items) // 2
    unsorted_left = items[:midpoint]
    unsorted_right = items[midpoint:]
    sorted_left = merge_sort(unsorted_left)
    sorted_right = merge_sort(unsorted_right)

    def _recursive_sort(
        l_sorted: List[models.ComparableElement],
        r_sorted: List[models.ComparableElement],
    ) -> List[models.ComparableElement]:
        if len(l_sorted) == 0 or len(r_sorted) == 0:
            return l_sorted if len(l_sorted) > 0 else r_sorted
        left, right = l_sorted[0], r_sorted[0]
        if left < right:
            return [left] + _recursive_sort(l_sorted[1:], r_sorted)
        return [right] + _recursive_sort(l_sorted, r_sorted[1:])

    result = _recursive_sort(sorted_left, sorted_right)
    return result
