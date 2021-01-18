from collections import deque
from log import log

class QueueFull(Exception):
    """An exception to raise when an item is inserted into an already full queue"""

class PriorityQueue():
    """A class representing a priority queue. Backed by deque (thread safe double-ended queue)
    Follows a traditional priority queue model, where elements are either floated up (on insert)
    or down (on dequeue) so that index 0 is the next element to be executed. Index > 0 implies
    they will be dequeued later.

    Parent/child relationship based on index:
                        0
                     /     \
                    1        2
                  /   \    /   \
                 3     4  5     6
    """

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
        self._comparator = comparator
        self._max_size = max_size
        self._queue = deque()

    def enqueue(self, item):
        """Inserts a new item into the queue. Inserts it into the correct position by using self.comparator and the parents value

            Args:
                item: Any object that adheres to self._comparator

            Returns:
        """
        if self._max_size <= 0 or len(self._queue) < self._max_size:
            self._queue.append(item)
            self._float_up(len(self._queue) - 1)
        else:
            log.error("Excluding inserting %s into PriorityQueue due to max_size being reached", item)
    
    def _swap(self, i1, i2):
        """
        """
        self._queue[i1], self._queue[i2] = self._queue[i2], self._queue[i1]

    def _float_up(self, index):
        """Given an index of an item, determines via self._comparator if it should be floated up (sooner execution) or not
        based on its parent's value.

        Args:
            index: Int that represents the index of the item to potentially float up

        Returns:
        """
        if index == 0:
            return
        parent_index = (index-1) // 2
        me = self._queue[index]
        parent = self._queue[parent_index]
        if self._comparator(me, parent):
            self._swap(index, parent_index)
            self._float_up(parent_index)

    def queue_sort(self):
        """Sorts the elements in the queue using dequeue. This means highest priority element
        will be at index 0, lowest priority element at index -1. This empties the queue.

        Returns:
            A list of elements sorted in order from highest priority to lowest
        """
        pass

    def set_max_size(self, new_size):
        """Sets a new max size for the PriorityQueue. See __init__ doc for implications. If
        there are more elements in the queue than new_size, will purge elements based on queue sort

        Args:
            new_size: int for max new size of the queue

        Returns:
        """
        self._max_size = new_size
        # have entries to purge
        if new_size >= 0 and new_size > len(self._queue):
            sorted_elements = self.queue_sort()
            for element in sorted_elements[:new_size]:
                self.enqueue(element)
