import dataclasses
from boards import board
from typing import Any, Iterable, List


@dataclasses.dataclass(frozen=True)
class NodePositionController:
    # fmt: off
    top_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("1"))
    top_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("2"))
    top_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("3"))
    mid_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("4"))
    mid_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("5"))
    mid_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("6"))
    bottom_left: board.Node = dataclasses.field(default_factory=lambda: board.Node("7"))
    bottom_centre: board.Node = dataclasses.field(default_factory=lambda: board.Node("8"))
    bottom_right: board.Node = dataclasses.field(default_factory=lambda: board.Node("9"))
    # fmt: on

    def __iter__(self) -> Iterable[board.Node]:
        field_names = [field.name for field in dataclasses.fields(self)]
        for field_name in field_names:
            yield getattr(self, field_name)

    def __str__(self) -> str:
        nodes = [node for node in self]
        content = ""
        for i in range(3):
            start = i * 3
            line = "\t".join([self._repr(nodes[j]) for j in range(start, start + 3)])
            content += f"{line}\n"
        return content

    def activate(self, active_node: board.Node) -> None:
        for node in self:
            if node.id == active_node.id:
                node.active = True
                node.visited = True
            else:
                node.activate = False

    def __post_init__(self):
        checked_list = []
        for node in self:
            if node.id in checked_list:
                raise ValueError(f"id: {node.id} has already been used")
            checked_list.append(node.id)

    def _repr(self, node: board.Node) -> str:
        if node.active:
            return "X"
        elif node.visited:
            return "1"
        return "0"


class AndroidBoard(board.Board):
    def __init__(self, controller: "NodePositionController"):
        self._controller = controller

    def __str__(self) -> str:
        return f"{type(self).__name__}(\n{str(self._controller)})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self._controller == other._controller

    def get_sequence(self) -> List[board.Node]:
        result = []
        for node in self._controller:
            if node.active:
                result.append(node)
                break
        current = result[0]
        while current.parent:
            current = current.parent
            result.insert(0, current)
        return result

    def get_next_boards(self) -> List[board.Board]:
        raise NotImplementedError
