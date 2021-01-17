# A module for some helpers for task frequency functions


def after_x_seconds(seconds):
    """Returns seconds as task frequency interval assumes seconds

    Args:
        seconds: int describing number of seconds to call tasks after

    Returns:
        int: seconds (no modification)
    """
    return seconds


def after_x_mintes(minutes):
    """Converts minutely frequency to seconds

    Args:
        minutes: int describing number of minutes to call tasks after

    Returns:
        int: seconds to call tasks after
    """
    return minutes * 60


def after_x_hours(hours):
    """Converts hourly frequency to seconds

    Args:
        hours: int describing number of hours to call tasks after

    Returns:
        int: seconds to call tasks after
    """

    return hours * 3600
