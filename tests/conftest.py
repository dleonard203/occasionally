import pytest
import occasionally
from occasionally.priority_queue import PriorityQueue

@pytest.fixture(scope="session")
def priority_min_queue():
    yield PriorityQueue(lambda x, y: x < y)
