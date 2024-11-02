import dataclasses
import pytest
from pyalgo import queue as queue_
from pyalgo.queue import queue as aqueue


@dataclasses.dataclass(frozen=True)
class MockElement:
    uid: str
    value: str


class TestFIFOQueue:
    @pytest.fixture
    def queue(self):
        queue = queue_.FIFOQueue[MockElement]()
        return queue

    def test_len(self, queue):
        elements = [MockElement("1", "1"), MockElement("2", "2"), MockElement("3", "3")]
        [queue.add(e) for e in elements]
        assert len(queue) == 3

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
        with pytest.raises(aqueue.EmptyQueueError):
            queue.get()
        with pytest.raises(KeyError):
            queue.remove("99")
