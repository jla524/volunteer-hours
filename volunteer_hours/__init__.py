"""
Package wide configurations
"""
import os
import sys
from typing import Optional
from pathlib import Path
from threading import Lock


class ThreadSafeMeta(type):
    """
    A thread-safe implementation of Singleton
    """
    _instances: dict = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
          the returned instance
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ThreadSafeMeta):
    """
    Global program configuration, uses the dotenv package to load runtime
      configuration from a .env file, once and only once into this object,
      this object can be used through-out the code base
    """
    try:
        __package = 'volunteer_hours'
        __version = '1.0.0'
        __default_env = 'dev'
        __logfile_name = f'{__package}-{__version}.log'
        __env = os.getenv('APP_ENV')
        __ragic_api_key = os.getenv('RAGIC_API_KEY')
        __config_dir = Path().home() / '.config' / __package
        __ragic_members_route = 'lynvolunteer/lyn-temp/53'
        __ragic_attendance_route = 'lynvolunteer/lyn-temp/9'
        __ragic_hours_detail = 'lynvolunteer/lyn-temp/55'
        __date_format = '%Y/%m/%d'
        __time_format = '%H:%M'
        __member_prefix = 'LYN'
    except KeyError as error:
        sys.stderr.write(f"Dotenv config error: {error} is missing\n")
        sys.exit(1)

    @classmethod
    def package(cls) -> str:
        """
        Getter for package name
        """
        return cls.__package

    @classmethod
    def version(cls) -> str:
        """
        Getter for version of package
        """
        return cls.__version

    @classmethod
    def default_env(cls) -> str:
        """
        Getter for default env
        """
        return cls.__default_env

    @classmethod
    def logfile_name(cls) -> str:
        """
        Getter for logging file name
        """
        return cls.__logfile_name

    @classmethod
    def env(cls) -> Optional[str]:
        """
        Getter for config
        """
        return cls.__env

    @classmethod
    def ragic_api_key(cls) -> Optional[str]:
        """
        Getter for Ragic API key
        """
        return cls.__ragic_api_key

    @classmethod
    def config_dir(cls) -> Path:
        """
        Getter for config directory
        """
        return cls.__config_dir

    @classmethod
    def ragic_members_route(cls) -> str:
        """
        Getter for members route
        """
        return cls.__ragic_members_route

    @classmethod
    def ragic_attendance_route(cls) -> str:
        """
        Getter for ragic attendance route
        """
        return cls.__ragic_attendance_route

    @classmethod
    def ragic_hours_detail(cls) -> str:
        """
        Getter for ragic hours detail
        """
        return cls.__ragic_hours_detail

    @classmethod
    def date_format(cls) -> str:
        """
        Getter for date format
        """
        return cls.__date_format

    @classmethod
    def time_format(cls) -> str:
        """
        Getter for time format
        """
        return cls.__time_format

    @classmethod
    def member_prefix(cls) -> str:
        """
        Getter for member prefix
        """
        return cls.__member_prefix
