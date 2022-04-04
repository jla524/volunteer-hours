"""
Enumerations for HTTP response codes and data fields
"""
# pylint: disable=R0903


class Http:
    """
    HTTP response codes
    """
    OK = 200
    CREATED = 201
    BAD = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404


class Members:
    """
    Members data fields
    """
    MEMBERSHIP_ID = 1003767


class Attendance:
    """
    Attendance data fields
    """
    MEMBERSHIP_ID = 1003777
    FIRST_NAME = 1003903
    LAST_NAME = 1003904
    EID = 1003807
    OPPORTUNITY = 1003809
    TIMECLOCK_STATUS = 1010008


class Hours:
    """
    Hours detail data fields
    """
    EID = 1003813
    DATE = 1003908
    EVENT_ID = 1003914
    EVENT_NAME = 1003915
    START_TIME = 1003910
    NEW_MEMBERSHIP_ID = 1003916
    END_TIME = 1003911
    STATUS = 1006691
