import abc
import dataclasses
from typing import Tuple, Union


class Coordinate(abc.ABC):
    @abc.abstractmethod
    def __add__(self, other: "Coordinate") -> "Coordinate":
        """Addition between two `Coordinate`s"""
        pass

    @abc.abstractmethod
    def __sub__(self, other: "Coordinate") -> "Coordinate":
        """Subtraction between two `Coordinate`s"""
        pass

    @abc.abstractmethod
    def __mul__(self, factor: Union[int, float]) -> "Coordinate":
        """Scalar multiplication with a given factor"""
        pass

    @abc.abstractmethod
    def __eq__(self, other: "Coordinate") -> bool:
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        pass

    @abc.abstractmethod
    def convert_tuple(self) -> Tuple[Union[int, float]]:
        pass


@dataclasses.dataclass
class Coordinate2D(Coordinate):
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(f"{self.x}, {self.y}")

    def __add__(self, other: "Coordinate2D") -> "Coordinate2D":
        return Coordinate2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coordinate2D") -> "Coordinate2D":
        return Coordinate2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]) -> "Coordinate2D":
        return Coordinate2D(int(self.x * other), int(self.y * other))

    def __lt__(self, other: "Coordinate2D") -> bool:
        return (self.x + self.y) < (other.x + other.y)

    def __eq__(self, other: "Coordinate2D") -> bool:
        return (
            isinstance(other, Coordinate2D) and self.x == other.x and self.y == other.y
        )

    def convert_tuple(self) -> Tuple[Union[int, float]]:
        return (self.x, self.y)

    def __post_init__(self):
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise ValueError(
                f"{type(self).__name__} must have arguments of class `int`"
            )
