from collections import deque
from log import log

class QueueFull(Exception):
    """An exception to raise when an item is inserted into an already full queue"""

class PriorityQueue():

    def __init__(self, comparator, max_size=0):
        """Creates a new PriorityQueue

        Args:
            comparator: a function for comparing two elements in the queue

            max_size: the maximum size the queue can be. If queue is at max size, and
            another element is attempted to be enqueued, that element will not (preserving existing elements).
            0 indicates no max size

        Returns:
            A new PriorityQueue
        """
        self._comparator = _comparator
        self._max_size = max_size
        self._queue = deque()

    def enqueue(self, item):
        """Inserts a new item into the queue. Inserts it into the correct position by using self.comparator and the parents value

            Args:
                item: Any object that adheres to self._comparator

            Returns:
        """
        if self.max_size and len(self.queue) < self.max_size:
            self.queue.append(item)
            self.float_up(len(self.queue) - 1)
        else:
            log.error("Excluding inserting %s into PriorityQueue due to max_size being reached", item)

    def float_up(self, index):
        """Given an index of an item, determines via self._comparator if it should be floated up (sooner execution) or not
        based on its parent's value.

        Args:
            index: Int that represents the index of the item to potentially float up

        Returns:
        """
        pass
