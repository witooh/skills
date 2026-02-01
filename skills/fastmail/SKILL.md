---
name: fastmail
description: Manages Fastmail email and calendar via JMAP and CalDAV APIs. Use when working with emails (read, send, reply, search, organize) or calendar events (create, list, update, delete, reminders). Supports Thai timezone (UTC+7).
compatibility: opencode
metadata:
  author: witooh
  version: "2.0"
  api: JMAP, CalDAV
---

## Quick Start

Invoke tools via CLI:

```bash
# Install dependencies first
cd .opencode/skills/fastmail && bun install

# Email: List mailboxes
bunx fastmail list_mailboxes

# Email: Send
bunx fastmail send_email \
  '{"to": [{"email": "user@example.com"}], "subject": "Hi", "body": "Message"}'

# Calendar: List events
bunx fastmail list_events \
  '{"start_date": "2024-01-01", "end_date": "2024-01-31"}'

# Calendar: Create event with reminder
bunx fastmail create_event_with_reminder \
  '{"title": "Meeting", "start": "2024-01-15T10:00:00", "end": "2024-01-15T11:00:00", "reminder_minutes": [15, 60]}'

# List all available tools
bunx fastmail --list
```

## When to Use This Skill

- 📧 Check inbox or search emails
- 📧 Send, reply, or move emails
- 🏷️ Apply labels or organize mailbox
- 📅 View calendar or events
- 📅 Create, update, or delete events
- 🔔 Set event reminders or alarms

## Email Tools (9 total)

| Tool | Purpose |
|------|---------|
| `list_mailboxes` | List all folders |
| `list_emails` | List emails in mailbox |
| `get_email` | Get full email content |
| `search_emails` | Search by text query |
| `send_email` | Send new email |
| `reply_email` | Reply to email |
| `move_email` | Move to folder |
| `set_labels` | Apply labels ($seen, $flagged) |
| `delete_email` | Delete (move to trash) |

## Calendar Tools (8 total)

| Tool | Purpose |
|------|---------|
| `list_calendars` | List all calendars |
| `list_events` | List events by date range |
| `get_event` | Get event details |
| `create_event` | Create new event |
| `update_event` | Update existing event |
| `delete_event` | Delete event |
| `search_events` | Search by title/description |
| `create_recurring_event` | Create repeating event |

## Reminder Tools (4 total)

| Tool | Purpose |
|------|---------|
| `add_event_reminder` | Add reminder to event |
| `remove_event_reminder` | Remove reminder(s) |
| `list_event_reminders` | List reminders for event |
| `create_event_with_reminder` | Create event + reminder in one call |

## Common Examples

```bash
# Check inbox (limit 10)
bunx fastmail list_emails '{"limit": 10}'

# Search for emails
bunx fastmail search_emails '{"query": "invoice"}'

# Get specific email content
bunx fastmail get_email '{"email_id": "xxx"}'

# Create recurring event (daily for 10 days)
bunx fastmail create_recurring_event \
  '{"title": "Standup", "start": "2024-01-01T09:00:00", "end": "2024-01-01T09:30:00", "recurrence": "daily", "recurrence_count": 10}'
```

## Decision Tree

**Need to manage email?**
- List/search → `list_emails` or `search_emails`
- Read content → `get_email`
- Send/reply → `send_email` or `reply_email`
- Organize → `move_email`, `set_labels`, `delete_email`

**Need to manage calendar?**
- View → `list_calendars` or `list_events`
- Create → `create_event` or `create_recurring_event`
- Modify → `update_event`
- Delete → `delete_event`

**Need reminders?**
- Add to existing event → `add_event_reminder`
- Create event + reminder → `create_event_with_reminder` (faster)
- Manage → `list_event_reminders`, `remove_event_reminder`

## Output Format

All tools return JSON:

```json
{
  "success": true,
  "data": { /* tool-specific response */ },
  "timestamp": "2024-01-15T10:00:00+07:00"
}
```

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `FASTMAIL_API_TOKEN` | Email via JMAP | Yes (for email) |
| `FASTMAIL_USERNAME` | Calendar via CalDAV | Yes (for calendar) |
| `FASTMAIL_PASSWORD` | Calendar app password | Yes (for calendar) |

**Setup:**
```bash
export FASTMAIL_API_TOKEN="your-api-token"
export FASTMAIL_USERNAME="your-email@fastmail.com"
export FASTMAIL_PASSWORD="your-app-password"
```

## Timezone Support

⏰ **All calendar times in UTC+7 (Asia/Bangkok)**
- Input times assumed UTC+7
- Output times shown in UTC+7
- Stored internally as UTC

## See Also

- **Detailed reference:** `.opencode/skills/fastmail/references/TOOLS.md`
- **Full guide:** `.opencode/skills/fastmail/README.md`
- **Setup help:** Fastmail Settings → Privacy & Security → Integrations
