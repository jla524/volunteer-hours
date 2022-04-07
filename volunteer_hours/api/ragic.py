"""
A wrapper for the Ragic API
"""
from __future__ import annotations
from datetime import datetime

import requests

from volunteer_hours import Config
from volunteer_hours.logger.pkg_logger import Logger
from volunteer_hours.common.enums import Http, Members, Attendance, Hours


class Ragic:
    """
    Use the requests library to talk to the Ragic API
    """
    _base_url = 'https://na3.ragic.com'

    def _get_data(self, api_route: str, params: dict) -> requests.Response:
        """
        Get data from the specified API route
        :param api_route: an API route in Ragic
        :param params: parameters to send to Ragic
        :return: a response object from Ragic
        """
        url = f'{self._base_url}/{api_route}'
        api_key = Config.ragic_api_key()
        headers = {'Authorization': f'Basic {api_key}'}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == Http.OK:
            Logger.info(f"Data sent to {url}.")
        return response

    def _send_data(self, api_route: str, data: dict) -> requests.Response:
        """
        Send data to the specified API route.
        :param api_route: an API route in Ragic
        :param data: data to send to Ragic
        :return: a response object from Ragic
        """
        url = f'{self._base_url}/{api_route}'
        api_key = Config.ragic_api_key()
        headers = {'Authorization': f'Basic {api_key}'}
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == Http.OK:
            Logger.info(f"Data sent to {url}.")
        return response

    def get_member_info(self, member_id: str) -> dict:
        """
        Get the current member's info
        :param member_id: the associated member ID
        :return: info of the member
        """
        route = Config.ragic_members_route()
        condition = [f'{Members.MEMBERSHIP_ID},eq,{member_id}']
        payload = {'where': condition, 'api': ''}

        response = self._get_data(route, payload)
        return response.json()

    def fetch_events(self, member_id: str) -> dict:
        """
        Retrieve active events that the member signed up for
        :param member_id: the associated member ID
        :return: events data from Ragic
        """
        route = Config.ragic_attendance_route()
        conditions = [f'{Attendance.TIMECLOCK_STATUS},eq,Open',
                      f'{Attendance.MEMBERSHIP_ID},eq,{member_id}']
        payload = {'where': conditions, 'api': ''}

        response = self._get_data(route, payload)
        return response.json()

    def _get_hours_detail(self, member_id: str, event_id: int) -> dict:
        """
        Get the hours detail of the current member
        :param member_id: the associated member ID
        :param event_id: the ID of the selected event
        :return: hours detail from Ragic
        """
        route = Config.ragic_hours_detail()
        date = datetime.now().strftime(Config.date_format())
        conditions = [f'{Hours.STATUS},eq,Incomplete',
                      f'{Hours.DATE},eq,{date}',
                      f'{Hours.EVENT_ID},eq,{event_id}',
                      f'{Hours.NEW_MEMBERSHIP_ID},eq,{member_id}']
        payload = {'where': conditions, 'api': ''}

        response = self._get_data(route, payload)
        return response.json()

    def _clock_in(self, eid: str, member_id: str, event_id: int) -> dict:
        """
        Clock in by creating a new record in hours detail
        :param member_id: the associated member ID
        :param event_id: the ID of the selected event
        :return: response data from Ragic
        """
        route = Config.ragic_hours_detail()
        now = datetime.now()
        date = now.strftime(Config.date_format())
        time = now.strftime(Config.time_format())
        payload = {Hours.EID: eid,
                   Hours.DATE: date,
                   Hours.EVENT_ID: event_id,
                   Hours.NEW_MEMBERSHIP_ID: member_id,
                   Hours.START_TIME: time}

        response = self._send_data(route, payload)
        return response.json()

    def _clock_out(self, record_id: str) -> dict:
        """
        Clock out by modifying an existing record in hours detail
        :param record_id: the ID of the record to modify
        :return: response data from Ragic
        """
        route = f'{Config.ragic_hours_detail()}/{record_id}'
        time = datetime.now().strftime(Config.time_format())
        payload = {Hours.END_TIME: time}

        response = self._send_data(route, payload)
        return response.json()

    def log_hours(self, member_id: str, event_id: int) -> str:
        """
        Clock in if the member is not clocked in, otherwise clock out
        :param member_id: the associated member ID
        :param event_id: the ID of the selected event
        :return: a message to the member
        """
        hours_info = self._get_hours_detail(member_id, event_id)
        record_id = list(hours_info.keys())[0] if hours_info else ''

        if record_id:
            self._clock_out(record_id)
            return "Clocked out successfully."

        attendance_info = self.fetch_events(member_id)
        event_details = list(attendance_info.values())[0]
        eid = event_details['EID']
        self._clock_in(eid, member_id, event_id)
        return "Clocked in successfully."
