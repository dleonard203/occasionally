from collections import deque
from log import log

class QueueFullException(Exception):
    """An exception to raise when an item is inserted into an already full queue"""

class QueueEmptyException(Exception):
    """An exception to raise when the queue is empty and someone tries to dequeue or peek"""

class PriorityQueue(object):
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

    def __repr__(self):
        return "PriorityQueue(%s, max_size=%r)" % (self._comparator.__name__, self._max_size)

    def __str__(self):
        return "#<PriorityQueue: max_size=%s comparator_function=%s>" % (self._max_size, self._comparator.__name__)

    def peek(self):
        """get the first element of the queue, and if no items exist, raises QueueEmptyException

        Args:

        Raises:
            QueueEmptyException

        Returns:
            First item in the queue. Can be any type
        """
        if len(self._queue) == 0:
            raise QueueEmptyException("%s is full" % self)
        return self._queue[0]

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
            raise QueueFullException("%s is full" % self)

    def dequeue(self):
        """Pops the top element off the queue, and replaces it with the next element in order. If
        no queue elements are in the queue, raises QueueEmptyException

        Args:

        Raises:
            QueueEmptyException

        Returns:
            Type of what has been fed to enqueue (any)
        """

        if len(self._queue) == 0:
            raise QueueEmptyException("%s is full" % self)
        # swap index 0 and -1 so we can float 0 (not guarenteed to be the top anymore) down
        self._swap(0, len(self._queue)-1)
        to_return = self._queue.pop()
        self._float_down(0)
        return to_return

    def _swap(self, i1, i2):
        """Swaps the order of self._queue[i1] and self._queue[i2]

        Args:
            i1: int first index to swap

            i2: int second index to swap

        Returns
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
        if self._comparator(me, parent) == me:
            self._swap(index, parent_index)
            self._float_up(parent_index)

    def _float_down(self, index):
        """Determines if a child is higher priority than index. If yes, swap, if no, terminate

        Args:
            index: int index in self._queue

        Returns:
        """

        # out of bounds
        if index < 0 or index >= len(self._queue):
            return

        me = self._queue[index]
        left_child_index = index*2 + 1
        right_child_index = index*2 + 2
        left_child = self._queue[left_child_index] if left_child_index < len(self._queue) else None
        right_child = self._queue[right_child_index] if right_child_index < len(self._queue) else None

        # no children
        if not left_child and not right_child:
            return

        # only left child exists
        if not right_child:
            # child has priority over index -- swap them
            if self._comparator(me, left_child) == left_child:
                self._swap(index, left_child_index)
                self._float_down(left_child_index)
        # both children exist
        else:
            highest_priority = self._comparator(right_child, left_child)
            highest_index = right_child_index if highest_priority == right_child else left_child_index
            # index is above highest priority -- swap them
            if self._comparator(highest_priority, me) == highest_priority:
                self._swap(highest_index, index)
                self._float_down(highest_index)


    def queue_sort(self):
        """Sorts the elements in the queue using dequeue. This means highest priority element
        will be at index 0, lowest priority element at index -1. This empties the queue.

        Args:

        Returns:
            A list of elements sorted in order from highest priority to lowest
        """
        to_return = list()
        while len(self._queue) > 0:
            to_return.append(self.dequeue())
        return to_return

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
