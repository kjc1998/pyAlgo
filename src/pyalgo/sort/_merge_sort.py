from typing import List
from pyalgo.sort import comparable


def merge_sort(items: List[comparable.Comparable]) -> List[comparable.Comparable]:
    if len(items) <= 1:
        return items

    midpoint = len(items) // 2
    unsorted_left = items[:midpoint]
    unsorted_right = items[midpoint:]
    sorted_left = merge_sort(unsorted_left)
    sorted_right = merge_sort(unsorted_right)

    def _recursive_sort(
        l_sorted: List[comparable.Comparable],
        r_sorted: List[comparable.Comparable],
    ) -> List[comparable.Comparable]:
        if len(l_sorted) == 0 or len(r_sorted) == 0:
            return list(l_sorted) if len(l_sorted) > 0 else list(r_sorted)
        left, right = l_sorted[0], r_sorted[0]
        if left < right:
            return [left] + _recursive_sort(l_sorted[1:], r_sorted)
        return [right] + _recursive_sort(l_sorted, r_sorted[1:])

    result = _recursive_sort(sorted_left, sorted_right)
    return result
