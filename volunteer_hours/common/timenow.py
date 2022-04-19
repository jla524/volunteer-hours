"""
A helper file for retrieving current date and time in the configured timezone.
"""
from datetime import datetime

from pytz import timezone, tzinfo

from volunteer_hours import Config


class LocalTime:
    """
    A wrapper for the datetime module
    """
    def __init__(self):
        self.__timezone = timezone(Config.timezone_name())

    @property
    def timezone(self) -> tzinfo:
        """
        Getter for timezone object
        :return: a timezone object with the configured timezone
        """
        return self.__timezone

    def today(self) -> str:
        """
        Get today's date in string format
        :return: today's date in the configured timezone
        """
        local_date = datetime.today().astimezone(self.timezone)
        return local_date.strftime(Config.date_format())

    def now(self) -> str:
        """
        Get the time now in string format
        :return: time now in the configured timezone
        """
        local_time = datetime.today().astimezone(self.timezone)
        return local_time.strftime(Config.time_format())
