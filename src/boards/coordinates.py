import dataclasses
from typing import Any


@dataclasses.dataclass
class TwoIndex:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(f"{self.x}, {self.y}")

    def __add__(self, other: "TwoIndex") -> "TwoIndex":
        return TwoIndex(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "TwoIndex") -> "TwoIndex":
        return TwoIndex(self.x - other.x, self.y - other.y)

    def __lt__(self, other: "TwoIndex") -> bool:
        return (self.x + self.y) < (other.x + other.y)

    def __post_init__(self):
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise ValueError(
                f"{type(self).__name__} must have arguments of class `int`"
            )
