import pytest
import dataclasses
from pyalgo.queue import priority


class TestPriorityQueue:
    @pytest.fixture
    def queue(self):
        return priority.PriorityQueue[priority.SampleData]()

    def test_roundtrip(self, queue):
        e1 = priority.SampleData("1", 4)
        e2 = priority.SampleData("2", 7)
        e3 = priority.SampleData("3", 1)
        provided = [e1, e2, e3]

        [queue.add(i) for i in provided]
        assert len(queue) == 3

        expected = [e2, e1, e3]
        observed = [queue.get() for _ in range(len(provided))]
        assert expected == observed
