from typing import List
from pyalgo.sort import comparable


def quick_sort(items: List[comparable.Comparable]) -> List[comparable.Comparable]:
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
