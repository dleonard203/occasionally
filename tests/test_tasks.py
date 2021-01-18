import time
import pytest
from occasionally.task import Task, MaxCallException

def mutate_dict(d, k, v):
    # dict[key] = value. lambda's can't have assignments in them
    d[k] = v

def raise_exception():
    raise Exception("Error")

def empty():
    pass

def test_testable_task():
    mutable_obj = dict()
    t = Task(mutate_dict, lambda: 5, call_args=(mutable_obj, "test", 1))
    t.invoke()
    assert mutable_obj == {"test": 1}
    now = time.time()
    t.set_next_invoke()
    assert abs(t._next_invoke - now - 5) < 1  # function should invoke within next 5 seconds +/- process time

def test_exception_cleanup():
    mutable_obj = dict()
    exception_handler = Task(mutate_dict, None, call_args=(mutable_obj, "test", 2))
    # the task always raises an exception, so the exception_handler will always be called
    t = Task(raise_exception, lambda: 5, exception_handler=exception_handler)
    t.invoke()
    assert mutable_obj == {"test": 2}

def test_next_task():
    mutable_obj = dict()
    next_task = Task(mutate_dict, None, call_args=(mutable_obj, "test", 3))
    t = Task(empty, lambda: 5, next_task=next_task)
    t.invoke()
    # since empty does nothing, it will not fail, and next_task should be called
    assert mutable_obj == {"test": 3}

def test_next_task_on_exception():
    mutable_obj = dict()
    next_task = Task(mutate_dict, None, call_args=(mutable_obj, "test", 4))
    t = Task(raise_exception, lambda: 5, next_task=next_task, call_next_task_on_exception=True)
    t.invoke()
    # next_task should be invoked even on error
    assert mutable_obj == {"test": 4}

def test_max_invoke():
    t = Task(empty, lambda: 5, just_x_times=1)
    t.invoke()
    with pytest.raises(MaxCallException):
        t.set_next_invoke()
    with pytest.raises(MaxCallException):
        t.invoke()
