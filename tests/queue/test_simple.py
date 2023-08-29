import dataclasses
import pytest
from pyalgo.queue import simple


@dataclasses.dataclass
class MockElement:
    uid: str
    value: str


class TestSimpleQueue:
    @pytest.fixture
    def queue(self):
        queue = simple.SimpleQueue[MockElement]()
        return queue

    def test_round_trip(self, queue):
        element = MockElement("1234", "4321")
        queue.add(element)
        observed = queue.get()
        assert observed == element

    def test_remove(self, queue):
        elements = [MockElement("1", "1"), MockElement("2", "2"), MockElement("3", "3")]
        [queue.add(e) for e in elements]
        queue.remove("2")
        assert queue.get() == MockElement("1", "1")
        assert queue.get() == MockElement("3", "3")
        with pytest.raises(simple.EmptyQueueError):
            queue.get()
