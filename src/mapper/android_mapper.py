import functools
import coordinates, coordinate_operators
from mapper import mapper
from typing import Callable, Dict, Iterable, List, Optional

Coordinate2D = coordinates.Coordinate2D


class NonUniqueError(ValueError):
    def __init__(self, non_unique_ids: List[str]):
        msg = f"Repeated uids: {', '.join(non_unique_ids)}"
        super().__init__(msg)


def unique_id(cls: Callable):
    @functools.wraps(cls)
    def build_class_nodes(*nodes: mapper.Node):
        node_ids = [n.uid for n in nodes]
        uids = set(node_ids)
        if len(uids) != len(node_ids):
            non_unique_ids = [x for x in uids if node_ids.count(x) > 1]
            raise NonUniqueError(non_unique_ids)
        return cls(*nodes)

    return build_class_nodes


@unique_id
class AndroidMapper(mapper.Mapper):
    """Mapper for Android phone lock patterns"""

    def __init__(self, *nodes: mapper.Node):
        if len(nodes) != 9:
            raise ValueError(f"Required 9 nodes, only {len(nodes)} given")
        coords = [coordinates.Coordinate2D(i, j) for i in range(3) for j in range(3)]
        node_uids = [n.uid for n in nodes]
        self._coordinate_node_map = dict(zip(coords, node_uids))

    def get_next_uids(
        self, node_id: str, visited_uids: Optional[List[str]] = None
    ) -> Iterable[str]:
        map = self._generate_map()
        line_coords = map[node_id]
        visited_uids = visited_uids if visited_uids else []

        for coords in line_coords.values():
            for coord in coords:
                node_uid = self._coordinate_node_map[coord]
                if node_uid not in visited_uids:
                    yield node_uid
                    break

    def _generate_map(self) -> Dict[str, Dict[Coordinate2D, List[Coordinate2D]]]:
        if not hasattr(self, "_map"):
            self._map = {}
            coords = list(self._coordinate_node_map.keys())
            edge_coords = coordinate_operators.get_edge_coordinates(coords)

            for coord, node_uid in self._coordinate_node_map.items():
                gradients = self._get_edge_gradients(coord, edge_coords)
                gradient_line_coords = {
                    g: coordinate_operators.get_line_coordinates(
                        coords, coord, unit_gradient=g
                    )
                    for g in gradients
                }
                self._map[node_uid] = gradient_line_coords
        return self._map

    def _get_edge_gradients(
        self, ref_coord: Coordinate2D, edges: List[Coordinate2D]
    ) -> Dict[Coordinate2D, List[Coordinate2D]]:
        result = {
            coordinate_operators.get_unit_gradient(ref_coord, edge)
            for edge in edges
            if ref_coord != edge
        }
        return result
