#!/usr/bin/env python3
"""Fastmail CLI - Email & Calendar Management."""

from __future__ import annotations

import json
import os
import sys

# Allow running as `python scripts/cli.py` from the skill root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from scripts.jmap_client import JMAPClient
from scripts.caldav_client import CalDAVClient
from scripts.tools.email import EmailTools
from scripts.tools.calendar import CalendarTools
from scripts.errors import format_error, NotFoundError

# ---------------------------------------------------------------------------
# Lazy-initialized clients
# ---------------------------------------------------------------------------

_email_tools: EmailTools | None = None
_calendar_tools: CalendarTools | None = None


def _get_email_tools() -> EmailTools:
    global _email_tools
    if not _email_tools:
        token = os.environ.get("FASTMAIL_API_TOKEN")
        if not token:
            raise RuntimeError("FASTMAIL_API_TOKEN environment variable is required")
        _email_tools = EmailTools(JMAPClient(token))
    return _email_tools


def _get_calendar_tools() -> CalendarTools:
    global _calendar_tools
    if not _calendar_tools:
        username = os.environ.get("FASTMAIL_USERNAME")
        password = os.environ.get("FASTMAIL_PASSWORD")
        if not username or not password:
            raise RuntimeError("FASTMAIL_USERNAME and FASTMAIL_PASSWORD environment variables are required")
        _calendar_tools = CalendarTools(CalDAVClient(username, password))
    return _calendar_tools


# ---------------------------------------------------------------------------
# Tool dispatcher
# ---------------------------------------------------------------------------

def handle_tool(tool_name: str, args: dict) -> dict:
    try:
        name = tool_name if tool_name.startswith("fastmail_") else f"fastmail_{tool_name}"
        return _dispatch(name, args)
    except Exception as exc:
        return format_error(exc)


def _dispatch(name: str, args: dict) -> dict:  # noqa: C901
    # ── Email tools ────────────────────────────────────────────────────────
    if name == "fastmail_list_mailboxes":
        return {"success": True, "result": _get_email_tools().get_mailboxes()}

    if name == "fastmail_list_emails":
        return {"success": True, "result": _get_email_tools().list_emails(
            args.get("mailbox_id"), int(args.get("limit", 20)),
        )}

    if name == "fastmail_get_email":
        _require(args, "email_id")
        return {"success": True, "result": _get_email_tools().get_email(args["email_id"])}

    if name == "fastmail_search_emails":
        _require(args, "query")
        return {"success": True, "result": _get_email_tools().search_emails(
            args["query"], int(args.get("limit", 20)),
        )}

    if name == "fastmail_send_email":
        _require(args, "to", "subject", "text_body")
        return {"success": True, "result": _get_email_tools().send_email(
            to=args["to"], subject=args["subject"], text_body=args["text_body"],
            html_body=args.get("html_body"), cc=args.get("cc"), bcc=args.get("bcc"),
            in_reply_to=args.get("in_reply_to"), references=args.get("references"),
        )}

    if name == "fastmail_move_email":
        _require(args, "email_id", "target_mailbox_id")
        _get_email_tools().move_to_folder(
            args["email_id"], args["target_mailbox_id"], args.get("source_mailbox_id"),
        )
        return {"success": True, "result": {"message": "Email moved"}}

    if name == "fastmail_set_labels":
        _require(args, "email_id", "keywords")
        _get_email_tools().set_keywords(args["email_id"], args["keywords"])
        return {"success": True, "result": {"message": "Labels set"}}

    if name == "fastmail_delete_email":
        _require(args, "email_id")
        _get_email_tools().delete_email(args["email_id"])
        return {"success": True, "result": {"message": "Email deleted"}}

    if name == "fastmail_reply_email":
        _require(args, "email_id", "text_body")
        email = _get_email_tools()
        original = email.get_email(args["email_id"])
        sender = (original.get("from") or [{}])[0]
        if not sender:
            raise RuntimeError("Could not find sender information in original email")

        to_list: list[dict] = [sender]
        if args.get("reply_all"):
            to_list.extend(original.get("to") or [])
            to_list.extend(original.get("cc") or [])

        result = email.send_email(
            to=to_list, subject=args.get("subject") or f"Re: {original.get('subject', '')}",
            text_body=args["text_body"], html_body=args.get("html_body"),
            cc=args.get("cc"), bcc=args.get("bcc"), in_reply_to=args["email_id"],
        )
        return {"success": True, "result": result}

    if name == "fastmail_get_thread":
        _require(args, "email_id")
        return {"success": True, "result": _get_email_tools().get_thread(args["email_id"])}

    # ── Bulk email tools ───────────────────────────────────────────────────
    if name == "fastmail_bulk_move_emails":
        _require(args, "email_ids", "target_mailbox_id")
        return {"success": True, "result": _get_email_tools().bulk_move_to_folder(
            args["email_ids"], args["target_mailbox_id"], args.get("source_mailbox_id"),
        )}

    if name == "fastmail_bulk_set_labels":
        _require(args, "email_ids", "keywords")
        return {"success": True, "result": _get_email_tools().bulk_set_keywords(
            args["email_ids"], args["keywords"],
        )}

    if name == "fastmail_bulk_delete_emails":
        _require(args, "email_ids")
        return {"success": True, "result": _get_email_tools().bulk_delete_emails(args["email_ids"])}

    # ── Calendar tools ─────────────────────────────────────────────────────
    if name == "fastmail_list_calendars":
        return {"success": True, "result": _get_calendar_tools().list_calendars()}

    if name == "fastmail_list_events":
        return {"success": True, "result": _get_calendar_tools().list_events(
            args.get("calendar_id"), args.get("start_date"), args.get("end_date"),
        )}

    if name == "fastmail_get_event":
        _require(args, "event_id")
        return {"success": True, "result": _get_calendar_tools().get_event(args["event_id"])}

    if name == "fastmail_create_event":
        _require(args, "title", "start", "end")
        return {"success": True, "result": _get_calendar_tools().create_event(args.get("calendar_id"), args)}

    if name == "fastmail_update_event":
        _require(args, "event_id")
        event_id = args["event_id"]
        updates = {k: v for k, v in args.items() if k != "event_id"}
        _get_calendar_tools().update_event(event_id, updates)
        return {"success": True, "result": {"message": "Event updated"}}

    if name == "fastmail_delete_event":
        _require(args, "event_id")
        _get_calendar_tools().delete_event(args["event_id"])
        return {"success": True, "result": {"message": "Event deleted"}}

    if name == "fastmail_search_events":
        _require(args, "query")
        return {"success": True, "result": _get_calendar_tools().search_events(
            args["query"], args.get("start_date"), args.get("end_date"),
        )}

    if name == "fastmail_create_recurring_event":
        _require(args, "title", "start", "end", "recurrence")
        return {"success": True, "result": _get_calendar_tools().create_recurring_event(
            args.get("calendar_id"), args,
        )}

    if name == "fastmail_list_invitations":
        return {"success": True, "result": _get_calendar_tools().list_invitations()}

    if name == "fastmail_respond_to_invitation":
        _require(args, "event_id", "response")
        if args["response"] not in ("accept", "decline", "tentative"):
            raise ValueError("response must be one of: accept, decline, tentative")
        _get_calendar_tools().respond_to_invitation(args["event_id"], args["response"])
        return {"success": True, "result": {"message": f"Invitation {args['response']}ed"}}

    # ── Reminder tools ─────────────────────────────────────────────────────
    if name == "fastmail_add_event_reminder":
        _require(args, "event_id")
        return {"success": True, "result": _get_calendar_tools().add_reminder(args["event_id"], args)}

    if name == "fastmail_remove_event_reminder":
        _require(args, "event_id")
        _get_calendar_tools().remove_reminder(args["event_id"], args.get("reminder_id"))
        return {"success": True, "result": {"message": "Reminder removed"}}

    if name == "fastmail_list_event_reminders":
        _require(args, "event_id")
        return {"success": True, "result": _get_calendar_tools().list_reminders(args["event_id"])}

    if name == "fastmail_create_event_with_reminder":
        _require(args, "title", "start", "end")
        reminders = args.get("reminders")
        if not reminders:
            raise ValueError("At least one reminder is required")
        return {"success": True, "result": _get_calendar_tools().create_event(args.get("calendar_id"), args)}

    return {"success": False, "error": f"Unknown tool: {name}"}


def _require(args: dict, *keys: str) -> None:
    missing = [k for k in keys if not args.get(k)]
    if missing:
        raise ValueError(f"{', '.join(missing)} {'is' if len(missing) == 1 else 'are'} required")


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def _show_list() -> None:
    tools = [
        # Email (10)
        "list_mailboxes", "list_emails", "get_email", "get_thread",
        "search_emails", "send_email", "move_email", "set_labels",
        "delete_email", "reply_email",
        # Bulk (3)
        "bulk_move_emails", "bulk_set_labels", "bulk_delete_emails",
        # Calendar (10)
        "list_calendars", "list_events", "get_event", "create_event",
        "update_event", "delete_event", "search_events",
        "create_recurring_event", "list_invitations", "respond_to_invitation",
        # Reminder (4)
        "add_event_reminder", "remove_event_reminder",
        "list_event_reminders", "create_event_with_reminder",
    ]
    print("Available Tools (27 total):")
    sections = [
        ("Email Tools (10)", tools[:10]),
        ("Bulk Email Tools (3)", tools[10:13]),
        ("Calendar Tools (10)", tools[13:23]),
        ("Reminder Tools (4)", tools[23:]),
    ]
    idx = 1
    for title, items in sections:
        print(f"\n{title}:")
        for t in items:
            print(f"  {idx}. {t}")
            idx += 1


def _parse_args(argv: list[str]) -> tuple[str, dict]:
    command = argv[0]

    # Try JSON arg first
    if len(argv) >= 2 and argv[1].startswith(("{", "[")):
        try:
            params = json.loads(argv[1])
            if isinstance(params, dict):
                return command, params
        except json.JSONDecodeError:
            pass

    # Fall back to --key value parsing
    params: dict = {}
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg.startswith("--"):
            key = arg[2:]
            if "=" in key:
                k, v = key.split("=", 1)
                param = k.replace("-", "_")
                try:
                    params[param] = json.loads(v)
                except json.JSONDecodeError:
                    params[param] = v
            else:
                param = key.replace("-", "_")
                if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                    next_arg = argv[i + 1]
                    try:
                        params[param] = json.loads(next_arg)
                    except json.JSONDecodeError:
                        params[param] = next_arg
                    i += 1
                else:
                    params[param] = True
        i += 1

    return command, params


def main() -> None:
    argv = sys.argv[1:]

    if not argv or argv[0] == "--help":
        print(
            "Fastmail CLI - Email & Calendar Management\n\n"
            "USAGE:\n"
            "  python scripts/cli.py <command> [json_args | --flag value ...]\n\n"
            "  python scripts/cli.py --list        List all available tools\n\n"
            "ENVIRONMENT:\n"
            "  FASTMAIL_API_TOKEN     Required for email operations\n"
            "  FASTMAIL_USERNAME      Required for calendar operations\n"
            "  FASTMAIL_PASSWORD      Required for calendar operations\n\n"
            "OUTPUT:\n"
            "  JSON: { success: bool, result?: any, error?: string }"
        )
        sys.exit(0)

    if argv[0] == "--list":
        _show_list()
        sys.exit(0)

    command, params = _parse_args(argv)
    result = handle_tool(command, params)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
