"""Calendar operations via CalDAV."""

from __future__ import annotations

import os
import re
import sys
import uuid
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from ..caldav_client import CalDAVClient
from ..errors import NotFoundError


# ---------------------------------------------------------------------------
# Timezone helpers
# ---------------------------------------------------------------------------

def get_configured_timezone() -> str:
    """Return IANA timezone from env or system default."""
    if tz := os.environ.get("FASTMAIL_TIMEZONE"):
        return tz
    try:
        # datetime.now().astimezone() gives the local timezone with IANA key
        local_tz = datetime.now().astimezone().tzinfo
        if hasattr(local_tz, "key"):
            return local_tz.key
        return str(local_tz)
    except Exception:
        pass
    if tz := os.environ.get("TZ"):
        return tz
    return "UTC"


def _get_tz_offset(tz_name: str, dt: datetime | None = None) -> timedelta:
    """Get UTC offset for a timezone at a given datetime."""
    ref = dt or datetime.now(timezone.utc)
    if ref.tzinfo is None:
        ref = ref.replace(tzinfo=timezone.utc)
    tz = ZoneInfo(tz_name)
    return ref.astimezone(tz).utcoffset()


def _format_tz_offset(offset: timedelta) -> str:
    total_seconds = int(offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    total_seconds = abs(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{sign}{hours:02d}:{minutes:02d}"


# ---------------------------------------------------------------------------
# CalendarTools
# ---------------------------------------------------------------------------

class CalendarTools:
    def __init__(self, client: CalDAVClient):
        self._client = client
        self.timezone = get_configured_timezone()

    def get_timezone(self) -> str:
        return self.timezone

    # -- internal helpers ---------------------------------------------------

    @staticmethod
    def _get_obj_data(obj: object) -> str | None:
        """Extract ICS data string from a CalDAV object."""
        data = getattr(obj, "data", None)
        if data is None:
            return None
        return data if isinstance(data, str) else str(data)

    def _find_event_object(self, event_id: str) -> tuple[object, object, str]:
        """Find a CalDAV event object by ID across all calendars.

        Returns (calendar, obj, ics_data). Raises NotFoundError if not found.
        """
        calendars = self._client.get_calendars()
        for calendar in calendars:
            try:
                objects = self._client.fetch_calendar_objects(calendar)
                for obj in objects:
                    url_str = str(getattr(obj, "url", ""))
                    if event_id in url_str:
                        data = self._get_obj_data(obj)
                        if data:
                            return calendar, obj, data
            except Exception as e:
                print(f"Error searching in {getattr(calendar, 'name', '?')}: {e}", file=sys.stderr)
        raise NotFoundError("event", event_id)

    def _resolve_calendar(self, calendar_id: str | None) -> object:
        """Resolve a calendar by ID/name, or pick a suitable default."""
        calendars = self._client.get_calendars()
        if calendar_id:
            cal = self._client.get_calendar_by_id(calendar_id)
            if not cal:
                raise RuntimeError(f"Calendar not found: {calendar_id}")
            return cal
        calendar = next(
            (c for c in calendars
             if getattr(c, "name", "") and
             "task" not in (getattr(c, "name", "") or "").lower() and
             "default" not in (getattr(c, "name", "") or "").lower()),
            calendars[0] if calendars else None,
        )
        if not calendar:
            raise RuntimeError("No calendars found")
        return calendar

    @staticmethod
    def _existing_to_event_dict(existing: dict) -> dict:
        """Convert a parsed event dict into a dict suitable for _build_ical_event."""
        return {
            "title": existing["title"],
            "start": existing["start"],
            "end": existing["end"],
            "description": existing.get("description"),
            "location": existing.get("location"),
            "allDay": existing.get("isAllDay"),
            "attendees": existing.get("attendees"),
        }

    # -- timezone conversions -----------------------------------------------

    def _to_utc(self, local_date_str: str) -> str:
        """Convert local timezone datetime string to UTC ISO string."""
        date_str = local_date_str
        # Strip any existing timezone indicator — we treat input as configured tz
        date_str = re.sub(r'[+-]\d{2}:\d{2}$', '', date_str)
        date_str = re.sub(r'[+-]\d{4}$', '', date_str)
        date_str = date_str.rstrip("Z")

        parts = date_str.split("T")
        date_part = parts[0]
        time_part = parts[1] if len(parts) > 1 else "00:00:00"

        year, month, day = (int(x) for x in date_part.split("-"))
        time_components = time_part.split(":")
        hour = int(time_components[0])
        minute = int(time_components[1]) if len(time_components) > 1 else 0
        second = int(time_components[2].split(".")[0]) if len(time_components) > 2 else 0

        dt_as_utc = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
        offset = _get_tz_offset(self.timezone, dt_as_utc)
        utc_dt = dt_as_utc - offset
        return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _format_ical_date(self, dt: datetime, all_day: bool = False) -> str:
        if all_day:
            return dt.strftime("%Y%m%d")
        return dt.strftime("%Y%m%dT%H%M%SZ")

    def _parse_ical_date(self, ical_date: str, all_day: bool = False) -> str:
        if all_day:
            return f"{ical_date[:4]}-{ical_date[4:6]}-{ical_date[6:8]}"

        utc_dt = datetime.strptime(ical_date, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        offset = _get_tz_offset(self.timezone, utc_dt)
        local_dt = utc_dt + offset
        tz_str = _format_tz_offset(offset)
        return local_dt.strftime(f"%Y-%m-%dT%H:%M:%S{tz_str}")

    # -- duration / reminder helpers ----------------------------------------

    @staticmethod
    def _parse_duration_to_minutes(duration: str) -> int:
        is_negative = duration.startswith("-")
        clean = duration.lstrip("-")
        minutes = 0
        day_match = re.search(r"P(\d+)D", clean)
        if day_match:
            minutes += int(day_match.group(1)) * 24 * 60
        hour_match = re.search(r"(\d+)H", clean)
        if hour_match:
            minutes += int(hour_match.group(1)) * 60
        min_match = re.search(r"(\d+)M", clean)
        if min_match:
            minutes += int(min_match.group(1))
        return minutes if is_negative else -minutes

    @staticmethod
    def _build_trigger(options: dict) -> str:
        total_minutes = 0
        total_minutes += (options.get("daysBefore") or 0) * 24 * 60
        total_minutes += (options.get("hoursBefore") or 0) * 60
        total_minutes += options.get("minutesBefore") or 0
        if total_minutes == 0:
            total_minutes = 15

        days = total_minutes // (24 * 60)
        hours = (total_minutes % (24 * 60)) // 60
        mins = total_minutes % 60

        trigger = "-P"
        if days > 0:
            trigger += f"{days}D"
        if hours > 0 or mins > 0:
            trigger += "T"
            if hours > 0:
                trigger += f"{hours}H"
            if mins > 0:
                trigger += f"{mins}M"
        return trigger

    @staticmethod
    def _build_valarm(reminder: dict, reminder_id: str) -> str:
        trigger = CalendarTools._build_trigger(reminder)
        action = (reminder.get("action") or "display").upper()
        description = reminder.get("description") or "Event reminder"
        return (
            "BEGIN:VALARM\n"
            f"ACTION:{action}\n"
            f"TRIGGER:{trigger}\n"
            f"DESCRIPTION:{description}\n"
            f"X-WR-ALARMUID:{reminder_id}\n"
            "END:VALARM"
        )

    @staticmethod
    def _parse_valarms(ics_data: str) -> list[dict]:
        reminders: list[dict] = []
        for alarm in re.findall(r"BEGIN:VALARM[\s\S]*?END:VALARM", ics_data):
            reminder: dict = {}
            for line in alarm.split("\n"):
                trimmed = line.strip()
                if trimmed.startswith("TRIGGER:"):
                    reminder["trigger"] = trimmed[8:]
                    reminder["minutesBefore"] = CalendarTools._parse_duration_to_minutes(reminder["trigger"])
                elif trimmed.startswith("ACTION:"):
                    reminder["action"] = trimmed[7:].lower()
                elif trimmed.startswith("DESCRIPTION:"):
                    reminder["description"] = trimmed[12:]
                elif trimmed.startswith("X-WR-ALARMUID:"):
                    reminder["id"] = trimmed[14:]
            if "id" not in reminder:
                reminder["id"] = str(uuid.uuid4())
            if "trigger" in reminder:
                reminders.append(reminder)
        return reminders

    # -- ICS parsing / building ---------------------------------------------

    def _parse_event_data(self, ics_data: str, calendar_id: str, url: str, etag: str) -> dict:
        lines = ics_data.split("\n")
        event: dict = {"calendarId": calendar_id, "url": url, "etag": etag}
        in_event = False
        is_all_day = False

        for line in lines:
            trimmed = line.strip()
            if trimmed == "BEGIN:VEVENT":
                in_event = True
                continue
            if trimmed == "END:VEVENT":
                break
            if not in_event:
                continue

            if trimmed.startswith("UID:"):
                event["id"] = trimmed[4:]
            elif trimmed.startswith("SUMMARY:"):
                event["title"] = trimmed[8:]
            elif trimmed.startswith("DESCRIPTION:"):
                event["description"] = trimmed[12:]
            elif trimmed.startswith("LOCATION:"):
                event["location"] = trimmed[9:]
            elif trimmed.startswith("DTSTART;VALUE=DATE:"):
                is_all_day = True
                event["start"] = self._parse_ical_date(trimmed[19:], True)
            elif trimmed.startswith("DTSTART:"):
                event["start"] = self._parse_ical_date(trimmed[8:], False)
            elif trimmed.startswith("DTEND;VALUE=DATE:"):
                event["end"] = self._parse_ical_date(trimmed[17:], True)
            elif trimmed.startswith("DTEND:"):
                event["end"] = self._parse_ical_date(trimmed[6:], False)
            elif trimmed.startswith("RRULE:"):
                event["recurrence"] = trimmed[6:]

        event["isAllDay"] = is_all_day
        event["reminders"] = self._parse_valarms(ics_data)
        return event

    def _build_ical_event(
        self,
        event: dict,
        event_id: str,
        recurrence: str | None = None,
        reminders: list[dict] | None = None,
    ) -> str:
        start_utc = self._to_utc(event["start"])
        end_utc = self._to_utc(event["end"])
        start_dt = datetime.fromisoformat(start_utc)
        end_dt = datetime.fromisoformat(end_utc)

        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Fastmail CLI//EN",
            "CALSCALE:GREGORIAN",
            "BEGIN:VEVENT",
            f"UID:{event_id}",
        ]

        all_day = event.get("allDay") or event.get("all_day") or False
        if all_day:
            lines.append(f"DTSTART;VALUE=DATE:{self._format_ical_date(start_dt, True)}")
            lines.append(f"DTEND;VALUE=DATE:{self._format_ical_date(end_dt, True)}")
        else:
            lines.append(f"DTSTART:{self._format_ical_date(start_dt)}")
            lines.append(f"DTEND:{self._format_ical_date(end_dt)}")

        lines.append(f"SUMMARY:{event['title']}")

        if event.get("description"):
            lines.append(f"DESCRIPTION:{event['description']}")
        if event.get("location"):
            lines.append(f"LOCATION:{event['location']}")
        if recurrence:
            lines.append(f"RRULE:{recurrence}")

        for attendee in (event.get("attendees") or []):
            if attendee.get("name"):
                lines.append(f'ATTENDEE;CN="{attendee["name"]}":mailto:{attendee["email"]}')
            else:
                lines.append(f"ATTENDEE:mailto:{attendee['email']}")

        alarms = reminders if reminders is not None else (event.get("reminders") or [])
        for reminder in alarms:
            lines.append(self._build_valarm(reminder, str(uuid.uuid4())))

        lines.extend([
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
            "END:VEVENT",
            "END:VCALENDAR",
        ])
        return "\n".join(lines)

    # -- public API ---------------------------------------------------------

    def list_calendars(self) -> list[dict]:
        calendars = self._client.get_calendars()
        return [
            {
                "id": str(cal.url),
                "name": getattr(cal, "name", None) or "Unnamed Calendar",
                "description": getattr(cal, "description", None),
                "color": getattr(cal, "calendar_color", None),
                "timezone": getattr(cal, "timezone", None),
            }
            for cal in calendars
        ]

    def list_events(
        self,
        calendar_id: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict]:
        if calendar_id:
            cal = self._client.get_calendar_by_id(calendar_id)
            if not cal:
                raise RuntimeError(f"Calendar not found: {calendar_id}")
            target_calendars = [cal]
        else:
            target_calendars = self._client.get_calendars()

        effective_start = start_date
        effective_end = end_date

        if start_date and "T" not in start_date:
            effective_start = f"{start_date}T00:00:00"
        if end_date and "T" not in end_date:
            effective_end = f"{end_date}T23:59:59"
        elif start_date and not end_date:
            date_part = start_date.split("T")[0]
            effective_end = f"{date_part}T23:59:59"

        time_range = {
            "start": self._to_utc(effective_start) if effective_start else datetime.now(timezone.utc).isoformat(),
            "end": self._to_utc(effective_end) if effective_end else (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        }

        all_events: list[dict] = []
        for calendar in target_calendars:
            try:
                objects = self._client.fetch_calendar_objects(calendar, time_range)
                for obj in objects:
                    data = self._get_obj_data(obj)
                    if data:
                        url_str = str(getattr(obj, "url", ""))
                        etag = getattr(obj, "etag", "") or ""
                        event = self._parse_event_data(data, str(calendar.url), url_str, etag)
                        all_events.append(event)
            except Exception as e:
                print(f"Error fetching events from {getattr(calendar, 'name', '?')}: {e}", file=sys.stderr)

        all_events.sort(key=lambda ev: ev.get("start", ""))
        return all_events

    def get_event(self, event_id: str) -> dict:
        calendar, obj, data = self._find_event_object(event_id)
        url_str = str(getattr(obj, "url", ""))
        etag = getattr(obj, "etag", "") or ""
        return self._parse_event_data(data, str(calendar.url), url_str, etag)

    def create_event(self, calendar_id: str | None, options: dict) -> dict:
        calendar = self._resolve_calendar(calendar_id)
        event_id = str(uuid.uuid4())
        ics_data = self._build_ical_event(options, event_id)
        self._client.create_event(calendar, ics_data, event_id)
        return {"id": event_id}

    def update_event(self, event_id: str, updates: dict) -> None:
        calendar, obj, data = self._find_event_object(event_id)
        url_str = str(getattr(obj, "url", ""))
        etag = getattr(obj, "etag", "") or ""
        existing = self._parse_event_data(data, str(calendar.url), url_str, etag)

        merged = self._existing_to_event_dict(existing)
        merged["title"] = updates.get("title") or merged["title"]
        merged["start"] = updates.get("start") or merged["start"]
        merged["end"] = updates.get("end") or merged["end"]
        if "description" in updates:
            merged["description"] = updates["description"]
        if "location" in updates:
            merged["location"] = updates["location"]
        if "allDay" in updates:
            merged["allDay"] = updates["allDay"]
        if "attendees" in updates:
            merged["attendees"] = updates["attendees"]

        ics_data = self._build_ical_event(merged, event_id, existing.get("recurrence"))
        self._client.update_event(calendar, obj, ics_data)

    def delete_event(self, event_id: str) -> None:
        _calendar, obj, _data = self._find_event_object(event_id)
        self._client.delete_event(obj)

    def search_events(self, query: str, start_date: str | None = None, end_date: str | None = None) -> list[dict]:
        events = self.list_events(None, start_date, end_date)
        lower_query = query.lower()
        return [
            ev for ev in events
            if lower_query in (ev.get("title") or "").lower()
            or lower_query in (ev.get("description") or "").lower()
            or lower_query in (ev.get("location") or "").lower()
        ]

    def create_recurring_event(self, calendar_id: str | None, options: dict) -> dict:
        calendar = self._resolve_calendar(calendar_id)

        rrule = f"FREQ={options['recurrence'].upper()}"
        count = options.get("recurrence_count") or options.get("recurrenceCount")
        until = options.get("recurrence_until") or options.get("recurrenceUntil")
        if count:
            rrule += f";COUNT={count}"
        elif until:
            until_utc = self._to_utc(f"{until}T23:59:59")
            until_dt = datetime.fromisoformat(until_utc)
            rrule += f";UNTIL={self._format_ical_date(until_dt)}"

        event_id = str(uuid.uuid4())
        ics_data = self._build_ical_event(options, event_id, rrule)
        self._client.create_event(calendar, ics_data, event_id)
        return {"id": event_id}

    def add_reminder(self, event_id: str, options: dict) -> dict:
        calendar, obj, data = self._find_event_object(event_id)
        url_str = str(getattr(obj, "url", ""))
        etag = getattr(obj, "etag", "") or ""
        existing = self._parse_event_data(data, str(calendar.url), url_str, etag)

        existing_reminders = [
            {"minutesBefore": r.get("minutesBefore"), "action": r.get("action"), "description": r.get("description")}
            for r in (existing.get("reminders") or [])
        ]
        all_reminders = existing_reminders + [options]

        merged = self._existing_to_event_dict(existing)
        ics_data = self._build_ical_event(merged, event_id, existing.get("recurrence"), all_reminders)
        self._client.update_event(calendar, obj, ics_data)
        return {"id": str(uuid.uuid4())}

    def remove_reminder(self, event_id: str, reminder_id: str | None = None) -> None:
        calendar, obj, data = self._find_event_object(event_id)
        url_str = str(getattr(obj, "url", ""))
        etag = getattr(obj, "etag", "") or ""
        existing = self._parse_event_data(data, str(calendar.url), url_str, etag)

        remaining: list[dict] = []
        if reminder_id and existing.get("reminders"):
            remaining = [
                {"minutesBefore": r.get("minutesBefore"), "action": r.get("action"), "description": r.get("description")}
                for r in existing["reminders"] if r.get("id") != reminder_id
            ]

        merged = self._existing_to_event_dict(existing)
        ics_data = self._build_ical_event(merged, event_id, existing.get("recurrence"), remaining)
        self._client.update_event(calendar, obj, ics_data)

    def list_reminders(self, event_id: str) -> list[dict]:
        event = self.get_event(event_id)
        return event.get("reminders") or []

    # -- invitation helpers -------------------------------------------------

    @staticmethod
    def _parse_organizer(ics_data: str) -> dict | None:
        match = re.search(r'ORGANIZER(?:;CN="?([^":]*)"?)?:mailto:([^\r\n]+)', ics_data, re.IGNORECASE)
        if match:
            return {"name": match.group(1) or None, "email": match.group(2)}
        return None

    @staticmethod
    def _parse_my_status(ics_data: str) -> str:
        match = re.search(r'ATTENDEE[^:]*PARTSTAT=([^;:\r\n]+)', ics_data, re.IGNORECASE)
        if match:
            status = match.group(1).lower()
            if status in ("accepted", "declined", "tentative", "needs-action"):
                return status
        return "needs-action"

    def list_invitations(self) -> list[dict]:
        calendars = self._client.get_calendars()
        invitations: list[dict] = []

        for calendar in calendars:
            try:
                objects = self._client.fetch_calendar_objects(calendar)
                for obj in objects:
                    data = self._get_obj_data(obj)
                    if data and "ORGANIZER" in data and "ATTENDEE" in data:
                        url_str = str(getattr(obj, "url", ""))
                        etag = getattr(obj, "etag", "") or ""
                        event = self._parse_event_data(data, str(calendar.url), url_str, etag)
                        organizer = self._parse_organizer(data)
                        my_status = self._parse_my_status(data)
                        if organizer:
                            invitations.append({
                                "eventId": event.get("id"),
                                "calendarId": str(calendar.url),
                                "title": event.get("title"),
                                "organizer": organizer,
                                "start": event.get("start"),
                                "end": event.get("end"),
                                "description": event.get("description"),
                                "location": event.get("location"),
                                "myStatus": my_status,
                            })
            except Exception as e:
                print(f"Error fetching invitations from {getattr(calendar, 'name', '?')}: {e}", file=sys.stderr)

        return invitations

    def respond_to_invitation(self, event_id: str, response: str) -> None:
        PARTSTAT_MAP = {"accept": "ACCEPTED", "decline": "DECLINED", "tentative": "TENTATIVE"}
        new_partstat = PARTSTAT_MAP[response]

        _calendar, obj, data = self._find_event_object(event_id)
        updated_ics = re.sub(
            r'ATTENDEE([^:]*?)PARTSTAT=[^;:\r\n]+',
            f'ATTENDEE\\1PARTSTAT={new_partstat}',
            data,
            flags=re.IGNORECASE,
        )
        if f"PARTSTAT={new_partstat}" not in updated_ics:
            updated_ics = re.sub(
                r'ATTENDEE([^:]*):mailto:',
                f'ATTENDEE\\1;PARTSTAT={new_partstat}:mailto:',
                updated_ics,
                flags=re.IGNORECASE,
            )
        # _find_event_object already found the calendar, update via obj directly
        obj.data = updated_ics
        obj.save()
