import occasionally

def insert_new_top(q, val):
    # type: (occasionally.priority_queue.PriorityQueue, any) -> None
    q.enqueue(val)
    assert q._queue[0] == val


def test_priority_min_queue(priority_min_queue):
    insert_new_top(priority_min_queue, 5)  # insert a 5 -- only element so at the top
    insert_new_top(priority_min_queue, 1)  # insert a 1 -- new top, so deque should be [1, 5]
    assert priority_min_queue._queue[1] == 5
    insert_new_top(priority_min_queue, -500)  # insert -500 -- new top again
    priority_min_queue.enqueue(-200)  # insert -200 -- -500 should still be tpo
    assert priority_min_queue._queue[0] == -500
