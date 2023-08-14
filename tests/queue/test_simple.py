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
