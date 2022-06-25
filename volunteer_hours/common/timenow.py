"""
A helper file for retrieving current date and time in the configured timezone.
"""
from datetime import datetime, date, time

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
        local_datetime = datetime.today().astimezone(self.timezone)
        return local_datetime.strftime(Config.date_format())

    def now(self) -> str:
        """
        Get the time now in string format
        :return: time now in the configured timezone
        """
        local_time = datetime.today().astimezone(self.timezone)
        return local_time.strftime(Config.time_format())

    def delta_minutes(self, before: str) -> int:
        """
        Get the time difference from before to now
        :param before: a time string in ISO format
        :return: time difference in minutes
        """
        start_time = datetime.combine(date.today(), time.fromisoformat(before))
        end_time = datetime.today().astimezone(self.timezone)
        return (end_time.replace(tzinfo=None) - start_time).seconds // 60
