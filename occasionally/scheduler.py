import time
from priority_queue import PriorityQueue
from task import Task, MaxCallException, soonest_task_comparator
from log import log


class Scheduler(PriorityQueue):

    def __init__(self, max_size=0, sleep_interval=0.5):
        """Initializes the Scheduler

        Args:
            max_size: int ax size for ocassionally.priority_queue.PriorityQueue

            sleep_interval: number for how long to sleep if the next task is not ready yet

        Returns:
            Scheduler object
        """
        super(Scheduler, self).__init__(soonest_task_comparator, max_size=max_size)
        self._sleep_interval = sleep_interval

    def add_task(self, task):
        # type: (Task) -> None
        """Takes in occasionally.task.Task, computes its next invoke time, then enqueues it into its
        priority queue.

        Args:
            task: ocassionally.task.Task to be enqueued

        Returns:
        """

        task.set_next_invoke()
        self.enqueue(task)

    def foreground(self):
        """The meat and potatoes. This takes all of the tasks in the queue, executes them, then re-enqueues them
        for their next execution. This is a blocking method call

        Args:

        Returns:
        """
        while len(self._queue) > 0:
            now = time.time()
            task = self.peek()  # type: Task
            # it is time to execute the task
            if task._next_invoke <= now:
                task = self.dequeue()
                task.invoke()

                try:
                    # task should be called again
                    task.set_next_invoke()
                    self.enqueue(task)
                except MaxCallException:
                    # task has hit its call limit and will not be invoked
                    log.info("Removing task %s due to max invokes of %d being reached", task, task._max_calls)
            # it is not time to call the task yet
            else:
                time.sleep(self._sleep_interval)
            log.info("The scheduler ran out of tasks and is returning from foreground")
