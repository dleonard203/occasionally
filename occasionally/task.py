import time
from log import log


class Task():

    def __init__(self, call_function, frequency_function, call_args=list(), call_kwargs=dict(), next_task=None, exception_handler=None, call_next_task_on_exception: False, schedule_immediately: False, just_x_times: -1):
        # type: (func, func, list, dict, Task, Task) -> Task
        """Creates a new task object. Made to be passed to a Scheduler object.

        Args:
            call_function: a function to be called every frequency_function sections.

            frequency_function: a function that when called, returns the frequency seconds for the given task.

            call_args: a list of args to be passed to call_function.

            call_kwargs: a dict of keyword args to be passed to the call function.

            next_task: A Task object to be called if this task's invocation is successful. Defaults to None.

            exception_handler: A Task object to be called in the event of an exception. Defaults to None.

            call_next_task_on_exception: A bool that indicates whether or not next_task should be called in the event of an
            exception in call_function.

            schedule_immediately: A bool that indicates when the scheduler starts, if it should execute the task now, or wait
            until one frequency_function cycle

            just_x_times: An int indicating the number of times to run a task
        """

        self._call_function = call_function
        self._frequency_function = frequency_function
        self._call_args = call_args
        self._call_kwargs = call_kwargs
        self._next_task = next_task
        self._exception_handler = exception_handler
        self._call_next_task_on_exception = call_next_task_on_exception
        self._max_calls = just_x_times
        self._successful_calls = 0
        self._unsuccessful_calls = 0
        self._next_invoke = None

    def __str__(self):
        return "#<Task: call_function=%s, frequency_function=%s>" % (self._call_function.__name__, self._frequency_function.__name__)

    def _invoke(self):
        """Invokes the call_function with its call_args and call_kwargs

        Args:

        Returns:
        """
        hit_exception = False
        try:
            rv = self._call_function(*self._call_args, **self._call_kwargs)
            log.debug("Successfully completed task %s", self)
            self._successful_calls += 1
        except Exception:
            hit_exception = True
            log.exception("Task %s hit exception:", self)
            if self._exception_handler:
                self._exception_handler._invoke()
            self._unsuccessful_calls += 1
        # if there is a next task, and this task was successful or doesn't care about exception, execute next task
        if self._next_task and (not hit_exception or self._call_next_task_on_exception):
            log.debug("Task %s invoking next_task %s", self, self._next_task)
            self._next_task._invoke()

    def set_next_invoke(self, immediately: False):
        """Sets the next time for the task on self._next_invoke

        Args:
            immediately: A bool that forces time.now() to be used for the invocation time instead of self._frequency_function

        Returns:
        """
        if immediately:
            self._next_invoke = time.now()
        else:
            self._next_invoke = self._frequency_function()

    @property
    def times_called(self):
        return self._unsuccessful_calls + self._successful_calls
