import pytest
import dataclasses
from pyalgo.queue import priority


@dataclasses.dataclass(frozen=True)
class MockWeightedElement:
    uid: str
    value: int

    def __eq__(self, other):
        return self.value == other.value

    def __mt__(self, other):
        return self.value > other.value

    def __me__(self, other):
        return self.value >= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value


class TestPriorityQueue:
    @pytest.fixture
    def queue(self):
        return priority.PriorityQueue[MockWeightedElement]()

    def test_roundtrip(self, queue):
        e1 = MockWeightedElement("1", 4)
        e2 = MockWeightedElement("2", 7)
        e3 = MockWeightedElement("3", 1)
        provided = [e1, e2, e3]

        [queue.add(i) for i in provided]
        assert len(queue) == 3

        expected = [e2, e1, e3]
        observed = [queue.get() for _ in range(len(provided))]
        assert expected == observed
