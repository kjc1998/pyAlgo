import dataclasses
import pytest
from pyalgo.queue import queue as queue_, simple


@dataclasses.dataclass
class MockElement:
    uid: str
    value: str


class TestSimpleQueue:
    @pytest.fixture
    def queue(self):
        queue = simple.SimpleQueue[MockElement]()
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
        with pytest.raises(queue_.EmptyQueueError):
            queue.get()

    def test_replace(self, queue):
        elements = [MockElement("1", "1"), MockElement("2", "2"), MockElement("3", "3")]
        [queue.add(e) for e in elements]
        queue.replace("2", MockElement("4", "5"))
        expected = [MockElement("1", "1"), MockElement("4", "5"), MockElement("3", "3")]
        observed = [queue.get() for _ in range(len(queue))]
        assert expected == observed
