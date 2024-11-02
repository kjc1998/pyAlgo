import pytest
import dataclasses
from pyalgo import queue


@dataclasses.dataclass(frozen=True)
class SampleData:
    uid: str
    value: int

    @property
    def weight(self) -> int:
        return self.value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value < other.value
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value <= other.value
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value > other.value
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value >= other.value
        return False


class TestPriorityQueue:
    @pytest.fixture
    def queue(self):
        return queue.PriorityQueue["SampleData"]()

    def test_roundtrip(self, queue):
        e1 = SampleData("1", 4)
        e2 = SampleData("2", 7)
        e3 = SampleData("3", 1)
        provided = [e1, e2, e3]

        [queue.add(i) for i in provided]
        assert len(queue) == 3

        expected = [e2, e1, e3]
        observed = [queue.get() for _ in range(len(provided))]
        assert expected == observed
