import time
import pytest
from occasionally.scheduler import Scheduler
from occasionally.task import Task
from occasionally.time_helpers import after_x_seconds


def test_scheduler_enqueue(scheduler):
    t1 = Task(None, None)
    t2 = Task(None, None)
    # scheduler compares off of _next_invoke times
    t1._next_invoke = 0
    t2._next_invoke = 1
    scheduler.enqueue(t1)
    scheduler.enqueue(t2)
    assert scheduler.peek() is t1


def test_scheduler_foreground(scheduler, empty):
    t1 = Task(empty, after_x_seconds(0.1), just_x_times=2)
    t2 = Task(empty, after_x_seconds(0.1), just_x_times=2)
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    now = time.time()
    scheduler.foreground()
    end = time.time()
    # executing two tasks twice with 0.1 second between tasks should not take more than 2 seconds
    assert end - now < 2
    assert t1.times_called == 2
    assert t2.times_called == 2


def append_to_list(l):
    l.append(time.time())


@pytest.mark.slow
def test_scheduler_foreground_frequency(scheduler):
    mutable_obj = list()
    t = Task(append_to_list, lambda: 1, just_x_times=5, call_args=(mutable_obj,))
    scheduler.add_task(t)
    scheduler.foreground()
    assert len(mutable_obj) == 5
    for index in range(4):
        this = mutable_obj[index]
        nxt = mutable_obj[index + 1]
        # task called once per second with .5 seconds sleep and .1 execution time leighway
        assert nxt - this < 1.6