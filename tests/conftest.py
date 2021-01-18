import pytest
import occasionally
from occasionally.priority_queue import PriorityQueue


def min_queue_comparator(x, y):
    return y if x > y else x

def max_queue_comparator(x, y):
    return x if x > y else y

@pytest.fixture
def priority_min_queue():
    yield PriorityQueue(min_queue_comparator)

@pytest.fixture
def priority_max_queue():
    yield PriorityQueue(max_queue_comparator)

@pytest.fixture
def small_max_queue():
    yield PriorityQueue(max_queue_comparator, max_size=2)
