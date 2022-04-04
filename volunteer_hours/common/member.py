"""
Define class for member
"""
from volunteer_hours import Config
from volunteer_hours.api.ragic import Ragic


class Member:
    """
    A member is an end user with a valid member ID
    """
    def __init__(self):
        self._member_id: str = ''
        self._events: dict[str, int] = {}

    @property
    def member_id(self) -> str:
        """
        Getter for member ID
        :return: stored member ID
        """
        return self._member_id

    @member_id.setter
    def member_id(self, member_id: str) -> None:
        """
        Setter for member ID
        :param member_id: a member ID
        :return: None
        """
        valid_prefix = Config.member_prefix()
        if member_id.startswith(valid_prefix):
            print(f"Setting member ID to {member_id}")
            self._member_id = member_id

    def reset_member(self) -> None:
        """
        Reset member ID and events to their original values
        :return: None
        """
        self._member_id = ''
        self._events = {}

    def get_member_name(self) -> str:
        """
        Get the first and last name of the member
        :return: the member's first and last name
        """
        result = Ragic().get_member_info(self._member_id)
        info = list(result.values())[0]
        return info['Full Name']

    def get_event_names(self) -> list[str]:
        """
        Get a list of events names assigned to the member
        :return: a list of events
        """
        if not self._member_id:
            return []

        events = Ragic().fetch_events(self._member_id)
        for event in events.values():
            self._events[event['Opportunity']] = event['Event ID']
        return list(self._events.keys())

    def get_event_id(self, event_name: str) -> int:
        """
        Find the event ID corresponding to the event name
        :return: an Event ID
        """
        if not self._events or event_name not in self._events:
            raise ValueError('Event not found')
        return self._events[event_name]
