# occasionally
A task scheduler and executioner for python 2.7 and 3+ using only the stdlib

Some environments are constrained, for example, an environment with no internet access. When developing for environments like this, the standard lib is the only tool you have to work with.

This package has two main classes that you will want: `ocassionally.tasks.Task` is a container for describing tasks. It takes a callable function (and its args and kwargs), and a frequency function to determine how often it should be called.

The `ocassionally.scheduler.Scheduler` class runs these Tasks at their set interval, backed by a priority queue. This queue calls a task when it is time, and reschedules it uses the Task's `frequency_function` to determine time until next call.

For example:

```python
from ocasionally.task import Task
from ocassionally.scheduler import Scheduler
from ocasionally.time_helper import after_x_minutes

def clean_db():
    # get rid of temp users that are created to trial the app. this is pseudo code
    with MyDbConnection() as db:
        db.Execute("DELETE FROM users WHERE temp_user = 1 AND logged_out = 1")

db_cleaner = ocassionally.task.Task(clean_db, after_x_mintes(5))  # makes a task that cleans the db every 5 minutes
Scheduler.add_task(db_cleaner)  # adds the task to the scheduler
Scheduler.foreground()  # start the scheduler running in foreground mode (main thread)
```

## Contributing
Since this package only relies on stdlib functionality, setup is pretty easy. On Linux:

1.) Setup virtual env (`virtualenv env`).

2.) Activate virtual env (`source env/bin/activate`).

3.) Run `./run_tests.sh` to run the tests and install the package in your virtualenv.

4.) Edit code in the `occasionally` folder, and make sure you the tests still pass with `./run_tests.sh`!

5.) Code is documented with the Google python style guide (https://google.github.io/styleguide/pyguide.html) and tests are implemented in pytest.
