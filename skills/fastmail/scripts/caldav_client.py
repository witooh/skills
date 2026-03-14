"""CalDAV client for Fastmail calendar operations using the caldav library."""

from __future__ import annotations

import sys
from datetime import datetime

import caldav


CALDAV_SERVER = "https://caldav.fastmail.com"


class CalDAVClient:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._client: caldav.DAVClient | None = None
        self._principal: caldav.Principal | None = None
        self._calendars: list[caldav.Calendar] | None = None

    def connect(self) -> None:
        if self._client:
            return

        self._client = caldav.DAVClient(
            url=CALDAV_SERVER,
            username=self._username,
            password=self._password,
        )
        self._principal = self._client.principal()
        print("Connected to Fastmail CalDAV", file=sys.stderr)

    def get_calendars(self) -> list[caldav.Calendar]:
        self.connect()
        if self._calendars is None:
            self._calendars = self._principal.calendars()
        return self._calendars

    def get_calendar_by_id(self, calendar_id: str) -> caldav.Calendar | None:
        calendars = self.get_calendars()
        for cal in calendars:
            if str(cal.url) == calendar_id or cal.name == calendar_id:
                return cal
        return None

    def fetch_calendar_objects(
        self,
        calendar: caldav.Calendar,
        time_range: dict[str, str] | None = None,
    ) -> list:
        self.connect()
        if time_range:
            start = datetime.fromisoformat(time_range["start"])
            end = datetime.fromisoformat(time_range["end"])
            return calendar.date_search(start=start, end=end, expand=True)
        return calendar.events()

    def create_event(self, calendar: caldav.Calendar, ics_data: str, _event_id: str = "") -> None:
        self.connect()
        calendar.save_event(ics_data)

    def update_event(self, calendar: caldav.Calendar, event: object, ics_data: str) -> None:
        self.connect()
        event.data = ics_data
        event.save()

    def delete_event(self, event: object) -> None:
        self.connect()
        event.delete()
