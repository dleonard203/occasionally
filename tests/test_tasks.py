import time
import pytest
from occasionally.task import Task

def mutate_dict(d, k, v):
    # dict[key] = value. lambda's can't have assignments in them
    d[k] = v

def test_testable_task():
    mutable_obj = dict()
    t = Task(mutate_dict, lambda: 5, call_args=(mutable_obj, "test", 5))
    t.invoke()
    assert mutable_obj == {"test": 5}
    now = time.time()
    t.set_next_invoke()
    assert abs(t._next_invoke - now - 5) < 1  # function should invoke within next 5 seconds +/- process time
