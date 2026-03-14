---
name: fastmail
description: Manages Fastmail email and calendar via JMAP and CalDAV APIs. Use for emails (read, send, reply, search, organize, bulk operations, threads) or calendar (events, reminders, RSVP invitations). Timezone auto-detected from system.
metadata:
  author: witooh
  version: "3.0"
  api: JMAP, CalDAV
---

## Quick Start

Invoke tools via CLI using the `Bash` tool:

```bash
# Install dependencies first (one-time setup)
cd <skill-directory>
uv venv .venv && uv pip install -r requirements.txt
# Or: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# Email: List mailboxes
.venv/bin/python scripts/cli.py list_mailboxes

# Email: Send
.venv/bin/python scripts/cli.py send_email \
  '{"to": [{"email": "user@example.com"}], "subject": "Hi", "text_body": "Message"}'

# Calendar: List events
.venv/bin/python scripts/cli.py list_events \
  '{"start_date": "2024-01-01", "end_date": "2024-01-31"}'

# Calendar: Create event with reminder
.venv/bin/python scripts/cli.py create_event_with_reminder \
  '{"title": "Meeting", "start": "2024-01-15T10:00:00+07:00", "end": "2024-01-15T11:00:00+07:00", "reminders": [{"minutesBefore": 15}, {"minutesBefore": 60}]}'

# List all available tools
.venv/bin/python scripts/cli.py --list
```

## When to Use This Skill

- Check inbox or search emails
- Send, reply, or move emails
- Apply labels or organize mailbox
- View calendar or events
- Create, update, or delete events
- Set event reminders or alarms

## Email Tools (10 total)

| Tool | Purpose |
| --- | --- |
| `list_mailboxes` | List all folders |
| `list_emails` | List emails in mailbox |
| `get_email` | Get full email content |
| `get_thread` | Get all emails in a conversation thread |
| `search_emails` | Search by text query |
| `send_email` | Send new email |
| `reply_email` | Reply to email |
| `move_email` | Move to folder |
| `set_labels` | Apply labels ($seen, $flagged) |
| `delete_email` | Delete (move to trash) |

## Bulk Email Tools (3 total)

| Tool | Purpose |
| --- | --- |
| `bulk_move_emails` | Move multiple emails at once |
| `bulk_set_labels` | Apply labels to multiple emails |
| `bulk_delete_emails` | Delete multiple emails at once |

## Calendar Tools (10 total)

| Tool | Purpose |
| --- | --- |
| `list_calendars` | List all calendars |
| `list_events` | List events by date range |
| `get_event` | Get event details |
| `create_event` | Create new event |
| `update_event` | Update existing event |
| `delete_event` | Delete event |
| `search_events` | Search by title/description |
| `create_recurring_event` | Create repeating event |
| `list_invitations` | List calendar invitations |
| `respond_to_invitation` | Accept/decline/maybe invitations |

## Reminder Tools (4 total)

| Tool | Purpose |
| --- | --- |
| `add_event_reminder` | Add reminder to event |
| `remove_event_reminder` | Remove reminder(s) |
| `list_event_reminders` | List reminders for event |
| `create_event_with_reminder` | Create event + reminder in one call |

## Common Examples

```bash
# Check inbox (limit 10)
.venv/bin/python scripts/cli.py list_emails '{"limit": 10}'

# Search for emails
.venv/bin/python scripts/cli.py search_emails '{"query": "invoice"}'

# Get specific email content
.venv/bin/python scripts/cli.py get_email '{"email_id": "xxx"}'

# Get email thread/conversation
.venv/bin/python scripts/cli.py get_thread '{"email_id": "xxx"}'

# Bulk operations
.venv/bin/python scripts/cli.py bulk_move_emails '{"email_ids": ["id1", "id2"], "target_mailbox_id": "archive"}'
.venv/bin/python scripts/cli.py bulk_delete_emails '{"email_ids": ["id1", "id2", "id3"]}'

# Create recurring event (daily for 10 days)
.venv/bin/python scripts/cli.py create_recurring_event \
  '{"title": "Standup", "start": "2024-01-01T09:00:00", "end": "2024-01-01T09:30:00", "recurrence": "daily", "recurrence_count": 10}'

# Calendar invitations
.venv/bin/python scripts/cli.py list_invitations
.venv/bin/python scripts/cli.py respond_to_invitation '{"event_id": "xxx", "response": "accept"}'
```

## Decision Tree

**Need to manage email?**

- List/search: `list_emails` or `search_emails`
- Read content: `get_email`
- View conversation: `get_thread`
- Send/reply: `send_email` or `reply_email`
- Organize: `move_email`, `set_labels`, `delete_email`
- Bulk actions: `bulk_move_emails`, `bulk_set_labels`, `bulk_delete_emails`

**Need to manage calendar?**

- View: `list_calendars` or `list_events`
- Create: `create_event` or `create_recurring_event`
- Modify: `update_event`
- Delete: `delete_event`
- Invitations: `list_invitations`, `respond_to_invitation`

**Need reminders?**

- Add to existing event: `add_event_reminder`
- Create event + reminder: `create_event_with_reminder` (faster)
- Manage: `list_event_reminders`, `remove_event_reminder`

## Output Format

All tools return JSON:

```json
{
  "success": true,
  "result": {
    /* tool-specific response */
  }
}
```

## Environment Variables

| Variable | Purpose | Required |
| --- | --- | --- |
| `FASTMAIL_API_TOKEN` | Email via JMAP | Yes (for email) |
| `FASTMAIL_USERNAME` | Calendar via CalDAV | Yes (for calendar) |
| `FASTMAIL_PASSWORD` | Calendar app password | Yes (for calendar) |
| `FASTMAIL_TIMEZONE` | Calendar timezone (IANA format) | No (auto-detected) |

**Setup:**

```bash
export FASTMAIL_API_TOKEN="your-api-token"
export FASTMAIL_USERNAME="your-email@fastmail.com"
export FASTMAIL_PASSWORD="your-app-password"
# Optional: Override timezone (defaults to system local timezone)
export FASTMAIL_TIMEZONE="America/New_York"  # or "Asia/Bangkok", "Europe/London", etc.
```

## Timezone Support

**Configurable calendar timezone**

- **Default:** Auto-detects your system's local timezone
- **Override:** Set `FASTMAIL_TIMEZONE` environment variable
- Uses IANA timezone identifiers (e.g., `America/New_York`, `Asia/Bangkok`, `Europe/London`)
- Input times assumed in configured timezone
- Output times shown in configured timezone
- Stored internally as UTC
- Handles Daylight Saving Time (DST) automatically

## See Also

- **Detailed reference:** `./references/TOOLS.md`
- **Setup help:** Fastmail Settings → Privacy & Security → Integrations
- **JMAP docs:** https://jmap.io/
- **CalDAV RFC:** https://datatracker.ietf.org/doc/html/rfc4791
