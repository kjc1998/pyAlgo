import itertools
import math
from typing import List
import coordinates

Coordinate = coordinates.Coordinate


def get_edge_coordinates(coordinates: List[Coordinate]) -> List[Coordinate]:
    """
    Finding the surrounding `Coordinate`s of a given shape (represented by list of `Coordinate`)
    Only valid for integer-based coordinates
    """
    result = set()
    coord_tuples = [c.convert_tuple() for c in coordinates]
    for i, coord in enumerate(coord_tuples):
        ranges = [(index - 1, index, index + 1) for index in coord]
        surrounding_coords = itertools.product(*ranges)
        for surrounding_coord in surrounding_coords:
            if surrounding_coord not in coord_tuples:
                result.add(coordinates[i])
                break
    return list(result)


def get_unit_gradient(ref_coord: Coordinate, end_coord: Coordinate) -> Coordinate:
    """
    Finding gradient between two `Coordinate`s
    """
    if ref_coord == end_coord:
        raise ValueError(f"Cannot find gradient for two identical points: {ref_coord}")
    diff = end_coord - ref_coord
    divisor = math.gcd(*diff.convert_tuple())  # find common divisor
    gradient = diff * (1 / divisor)
    return gradient


def get_line_coordinates(
    coordinates: List[Coordinate],
    ref_coord: Coordinate,
    end_coord: Coordinate = None,
    unit_gradient: Coordinate = None,
) -> List[Coordinate]:
    if (end_coord and unit_gradient) or (end_coord is None and unit_gradient is None):
        raise ValueError("Please provide either an end coordinate or a unit gradient")
    unit_gradient = (
        unit_gradient if unit_gradient else get_unit_gradient(ref_coord, end_coord)
    )
    result = []
    mutiplier = 1
    while True:
        next_coord = ref_coord + unit_gradient * mutiplier
        if next_coord == end_coord:
            result.append(next_coord)
            break
        elif next_coord in coordinates:
            result.append(next_coord)
            mutiplier += 1
        else:
            break
    return result
