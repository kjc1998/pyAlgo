from typing import Iterable, List
from pyalgo import models


def quick_sort(
    items: Iterable[models.ComparableElement],
) -> List[models.ComparableElement]:
    items_ = list(items)
    if len(items_) <= 1:
        return items_
    pivot = items_[-1]
    left, right = [], []
    for item in items_[:-1]:
        if item < pivot:
            left.append(item)
        else:
            right.append(item)
    return [*quick_sort(left), pivot, *quick_sort(right)]
