# Test Cases: Fastmail Skill

## Test Case Summary
- **Total Test Cases:** 46
- **Email Tools:** 19 test cases (TC-001 to TC-019)
- **Calendar Tools:** 14 test cases (TC-020 to TC-033)
- **Reminder Tools:** 5 test cases (TC-034 to TC-038)
- **Environment/Error:** 8 test cases (TC-039 to TC-046)

---

## Email Tools Test Cases

### TC-001: list_mailboxes - List All Mailboxes
**Priority:** P0  
**Type:** Functional  
**Tool:** `list_mailboxes`

#### Objective
Verify the tool returns all available mailboxes/folders with correct metadata

#### Preconditions
- FASTMAIL_API_TOKEN is set and valid
- Account has at least Inbox, Sent, Trash folders

#### Test Steps
1. Execute: `bunx fastmail list_mailboxes`

#### Expected Results
- Response contains `success: true`
- Returns array of mailbox objects
- Each mailbox has: `id`, `name`, `role`, `totalEmails`, `unreadEmails`
- At minimum includes: inbox, sent, trash (with correct role values)

---

### TC-002: list_emails - List Emails from Inbox (Default)
**Priority:** P0  
**Type:** Functional  
**Tool:** `list_emails`

#### Objective
Verify emails can be listed from default inbox with pagination

#### Preconditions
- FASTMAIL_API_TOKEN is set
- Inbox contains at least 5 emails

#### Test Steps
1. Execute: `bunx fastmail list_emails '{"limit": 5}'`

#### Expected Results
- Response contains `success: true`
- Returns array of 5 email objects
- Each email has: `id`, `from`, `subject`, `date`, `preview`, `isRead`
- Response includes `total` count field

---

### TC-003: list_emails - List Emails from Specific Mailbox
**Priority:** P0  
**Type:** Functional  
**Tool:** `list_emails`

#### Objective
Verify emails can be listed from a specific mailbox using mailbox_id

#### Preconditions
- TC-001 passed (have mailbox IDs)
- Sent folder has at least 1 email

#### Test Steps
1. Get mailbox ID for Sent folder from TC-001
2. Execute: `bunx fastmail list_emails '{"mailbox_id": "SENT_ID", "limit": 10}'`

#### Expected Results
- Returns emails only from specified mailbox
- Email subjects/content match Sent folder content

---

### TC-004: get_email - Retrieve Full Email Content
**Priority:** P0  
**Type:** Functional  
**Tool:** `get_email`

#### Objective
Verify full email content including headers, body, and attachments can be retrieved

#### Preconditions
- TC-002 passed (have email IDs)
- Have at least 1 email with attachments

#### Test Steps
1. Get email_id from TC-002
2. Execute: `bunx fastmail get_email '{"email_id": "EMAIL_ID"}'`

#### Expected Results
- Response contains full email object
- Fields present: `id`, `from`, `to`, `cc`, `subject`, `body`, `html`, `date`, `isRead`
- `from` is array of sender objects
- `to` and `cc` are arrays of recipient objects
- Attachments array present (even if empty)

---

### TC-005: get_thread - Retrieve Email Thread
**Priority:** P1  
**Type:** Functional  
**Tool:** `get_thread`

#### Objective
Verify email conversation thread can be retrieved

#### Preconditions
- Account has at least 1 email thread with 2+ messages

#### Test Steps
1. Identify an email that is part of a conversation thread
2. Execute: `bunx fastmail get_thread '{"email_id": "THREAD_EMAIL_ID"}'`

#### Expected Results
- Returns thread object with `id`, `emails[]`, `subject`, `participants[]`
- `emails` array contains all messages in thread
- `participants` lists all unique senders/recipients
- `emailCount` matches length of emails array

---

### TC-006: search_emails - Search by Text Query
**Priority:** P0  
**Type:** Functional  
**Tool:** `search_emails`

#### Objective
Verify email search by subject/body/sender text works

#### Preconditions
- Account has emails containing word "test" in subject or body

#### Test Steps
1. Execute: `bunx fastmail search_emails '{"query": "test", "limit": 20}'`

#### Expected Results
- Returns array of matching emails
- Each result contains matching content in preview
- `total` field shows total matches

---

### TC-007: search_emails - Search with No Results
**Priority:** P1  
**Type:** Negative  
**Tool:** `search_emails`

#### Objective
Verify search returns empty array when no matches found

#### Test Steps
1. Execute: `bunx fastmail search_emails '{"query": "XYZ_NONEXISTENT_12345"}'`

#### Expected Results
- `success: true`
- Returns empty `emails` array
- `total: 0`

---

### TC-008: send_email - Send Simple Email
**Priority:** P0  
**Type:** Functional  
**Tool:** `send_email`

#### Objective
Verify single recipient email can be sent successfully

#### Preconditions
- FASTMAIL_API_TOKEN is valid
- Test recipient email is accessible

#### Test Steps
1. Execute: `bunx fastmail send_email '{"to": [{"email": "test@example.com"}], "subject": "Test Email", "body": "This is a test email"}'`

#### Expected Results
- `success: true`
- Returns `emailId` for the sent message
- Email appears in Sent folder (verify via list_emails)

---

### TC-009: send_email - Send Email with CC and Multiple Recipients
**Priority:** P1  
**Type:** Functional  
**Tool:** `send_email`

#### Objective
Verify email with multiple TO and CC recipients works

#### Test Steps
1. Execute: `bunx fastmail send_email '{"to": [{"name": "User1", "email": "user1@test.com"}, {"email": "user2@test.com"}], "cc": [{"email": "cc@test.com"}], "subject": "Multi-recipient Test", "body": "Test with multiple recipients"}'`

#### Expected Results
- `success: true`
- All recipients receive the email

---

### TC-010: send_email - Send HTML Email
**Priority:** P1  
**Type:** Functional  
**Tool:** `send_email`

#### Objective
Verify HTML-formatted email can be sent

#### Test Steps
1. Execute: `bunx fastmail send_email '{"to": [{"email": "test@example.com"}], "subject": "HTML Test", "body": "Plain text fallback", "html": "<h1>HTML Email</h1><p>Formatted content</p>"}'`

#### Expected Results
- `success: true`
- Email contains HTML content when viewed in client

---

### TC-011: reply_email - Reply to Sender Only
**Priority:** P1  
**Type:** Functional  
**Tool:** `reply_email`

#### Objective
Verify reply to single sender works correctly

#### Preconditions
- Have an existing email_id from TC-004

#### Test Steps
1. Execute: `bunx fastmail reply_email '{"email_id": "EMAIL_ID", "body": "Thanks for your message!"}'`

#### Expected Results
- `success: true`
- Reply sent only to original sender
- Subject prefixed with "Re:"
- Proper In-Reply-To header set

---

### TC-012: reply_email - Reply All
**Priority:** P1  
**Type:** Functional  
**Tool:** `reply_email`

#### Objective
Verify reply-all includes all original recipients

#### Preconditions
- Have an existing email with multiple TO/CC recipients

#### Test Steps
1. Execute: `bunx fastmail reply_email '{"email_id": "EMAIL_ID", "body": "Replying to all", "reply_all": true}'`

#### Expected Results
- Reply sent to original sender AND all TO/CC recipients

---

### TC-013: move_email - Move Email to Different Folder
**Priority:** P1  
**Type:** Functional  
**Tool:** `move_email`

#### Objective
Verify email can be moved between mailboxes

#### Preconditions
- Have email_id from TC-002
- Have target mailbox_id from TC-001 (e.g., Archive)

#### Test Steps
1. Execute: `bunx fastmail move_email '{"email_id": "EMAIL_ID", "target_mailbox_id": "ARCHIVE_ID"}'`

#### Expected Results
- `success: true`
- Email no longer appears in original mailbox
- Email appears in target mailbox

---

### TC-014: set_labels - Mark Email as Read
**Priority:** P1  
**Type:** Functional  
**Tool:** `set_labels`

#### Objective
Verify email read/unread status can be toggled

#### Preconditions
- Have unread email_id

#### Test Steps
1. Execute: `bunx fastmail set_labels '{"email_id": "EMAIL_ID", "labels": {"$seen": true}}'`

#### Expected Results
- `success: true`
- Email marked as read in list_emails output
- `$seen` label applied

---

### TC-015: set_labels - Flag Email and Add Custom Label
**Priority:** P1  
**Type:** Functional  
**Tool:** `set_labels`

#### Objective
Verify multiple labels including custom labels can be applied

#### Test Steps
1. Execute: `bunx fastmail set_labels '{"email_id": "EMAIL_ID", "labels": {"$flagged": true, "Important": true}}'`

#### Expected Results
- Email flagged as important
- Custom "Important" label applied
- Can be seen in email metadata

---

### TC-016: delete_email - Delete Single Email
**Priority:** P1  
**Type:** Functional  
**Tool:** `delete_email`

#### Objective
Verify email can be deleted (moved to trash)

#### Preconditions
- Have email_id to delete (create a test email if needed)

#### Test Steps
1. Execute: `bunx fastmail delete_email '{"email_id": "EMAIL_ID"}'`

#### Expected Results
- `success: true`
- Email moved to Trash folder
- `deletedCount: 1`

---

### TC-017: bulk_move_emails - Move Multiple Emails
**Priority:** P1  
**Type:** Functional  
**Tool:** `bulk_move_emails`

#### Objective
Verify multiple emails can be moved at once

#### Preconditions
- Have at least 3 email_ids
- Have target mailbox_id

#### Test Steps
1. Execute: `bunx fastmail bulk_move_emails '{"email_ids": ["id1", "id2", "id3"], "target_mailbox_id": "TARGET_ID"}'`

#### Expected Results
- `success: true`
- `succeeded` array contains all email_ids
- `failed` array is empty
- All emails moved to target mailbox

---

### TC-018: bulk_set_labels - Apply Labels to Multiple Emails
**Priority:** P2  
**Type:** Functional  
**Tool:** `bulk_set_labels`

#### Objective
Verify labels can be applied to multiple emails at once

#### Test Steps
1. Execute: `bunx fastmail bulk_set_labels '{"email_ids": ["id1", "id2"], "labels": {"$seen": true}}'`

#### Expected Results
- All specified emails marked as read
- Partial failures reported in `failed` array if any

---

### TC-019: bulk_delete_emails - Delete Multiple Emails
**Priority:** P2  
**Type:** Functional  
**Tool:** `bulk_delete_emails`

#### Objective
Verify multiple emails can be deleted at once

#### Test Steps
1. Execute: `bunx fastmail bulk_delete_emails '{"email_ids": ["id1", "id2", "id3"]}'`

#### Expected Results
- All emails moved to trash
- `succeeded` array matches input email_ids
- `failed` array empty

---

## Calendar Tools Test Cases

### TC-020: list_calendars - List All Calendars
**Priority:** P0  
**Type:** Functional  
**Tool:** `list_calendars`

#### Objective
Verify all calendars are listed with metadata

#### Preconditions
- FASTMAIL_USERNAME and FASTMAIL_PASSWORD are set
- Account has at least Personal and Work calendars

#### Test Steps
1. Execute: `bunx fastmail list_calendars`

#### Expected Results
- `success: true`
- Returns array of calendar objects
- Each has: `id`, `name`, `color`, `isReadOnly`

---

### TC-021: list_events - List Events in Date Range
**Priority:** P0  
**Type:** Functional  
**Tool:** `list_events`

#### Objective
Verify events can be listed for a date range

#### Preconditions
- Calendar has events in current month

#### Test Steps
1. Execute: `bunx fastmail list_events '{"start_date": "2026-01-01", "end_date": "2026-01-31"}'`

#### Expected Results
- Returns events within date range
- Each event has: `id`, `title`, `start`, `end`, `description`, `location`, `isAllDay`
- Times shown in configured timezone

---

### TC-022: list_events - List Events from Specific Calendar
**Priority:** P1  
**Type:** Functional  
**Tool:** `list_events`

#### Objective
Verify events can be filtered by calendar

#### Preconditions
- TC-020 passed (have calendar IDs)

#### Test Steps
1. Execute: `bunx fastmail list_events '{"calendar_id": "CAL_ID", "start_date": "2026-01-01", "end_date": "2026-01-31"}'`

#### Expected Results
- Only events from specified calendar returned

---

### TC-023: get_event - Get Event Details
**Priority:** P0  
**Type:** Functional  
**Tool:** `get_event`

#### Objective
Verify full event details can be retrieved

#### Preconditions
- TC-021 passed (have event IDs)

#### Test Steps
1. Execute: `bunx fastmail get_event '{"event_id": "EVENT_ID"}'`

#### Expected Results
- Returns complete event object
- Includes: `id`, `title`, `start`, `end`, `description`, `location`, `isAllDay`, `calendar_id`, `reminders`

---

### TC-024: create_event - Create Simple Event
**Priority:** P0  
**Type:** Functional  
**Tool:** `create_event`

#### Objective
Verify new event can be created

#### Preconditions
- Valid CalDAV credentials

#### Test Steps
1. Execute: `bunx fastmail create_event '{"title": "Test Meeting", "start": "2026-02-15T10:00:00", "end": "2026-02-15T11:00:00"}'`

#### Expected Results
- `success: true`
- Returns `eventId`
- Event appears in list_events

---

### TC-025: create_event - Create Event with Description and Location
**Priority:** P1  
**Type:** Functional  
**Tool:** `create_event`

#### Objective
Verify event with full details can be created

#### Test Steps
1. Execute: `bunx fastmail create_event '{"title": "Project Review", "start": "2026-02-20T14:00:00", "end": "2026-02-20T15:30:00", "description": "Quarterly review meeting", "location": "Conference Room A"}'`

#### Expected Results
- Event created with all fields preserved

---

### TC-026: create_event - Create All-Day Event
**Priority:** P1  
**Type:** Functional  
**Tool:** `create_event`

#### Objective
Verify all-day event can be created

#### Test Steps
1. Execute: `bunx fastmail create_event '{"title": "Company Holiday", "start": "2026-03-01", "end": "2026-03-02", "all_day": true}'`

#### Expected Results
- Event created with `isAllDay: true`
- No time component in display

---

### TC-027: update_event - Update Event Details
**Priority:** P1  
**Type:** Functional  
**Tool:** `update_event`

#### Objective
Verify existing event can be updated

#### Preconditions
- TC-024 passed (have event_id)

#### Test Steps
1. Execute: `bunx fastmail update_event '{"event_id": "EVENT_ID", "title": "Updated Meeting Title", "location": "New Location"}'`

#### Expected Results
- `success: true`
- Changes reflected in get_event output

---

### TC-028: delete_event - Delete Event
**Priority:** P1  
**Type:** Functional  
**Tool:** `delete_event`

#### Objective
Verify event can be deleted

#### Preconditions
- Have event_id (create test event)

#### Test Steps
1. Execute: `bunx fastmail delete_event '{"event_id": "EVENT_ID"}'`

#### Expected Results
- `success: true`
- Event no longer appears in list_events
- `deletedCount: 1`

---

### TC-029: search_events - Search Events by Title
**Priority:** P1  
**Type:** Functional  
**Tool:** `search_events`

#### Objective
Verify events can be searched by title/description

#### Preconditions
- Calendar has events with "meeting" in title

#### Test Steps
1. Execute: `bunx fastmail search_events '{"query": "meeting"}'`

#### Expected Results
- Returns matching events
- Searches in both title and description

---

### TC-030: create_recurring_event - Create Daily Recurring Event
**Priority:** P1  
**Type:** Functional  
**Tool:** `create_recurring_event`

#### Objective
Verify recurring event can be created with count

#### Test Steps
1. Execute: `bunx fastmail create_recurring_event '{"title": "Daily Standup", "start": "2026-02-01T09:00:00", "end": "2026-02-01T09:30:00", "recurrence": "daily", "recurrence_count": 5}'`

#### Expected Results
- `success: true`
- Creates 5 instances of the event
- Visible in calendar for consecutive days

---

### TC-031: create_recurring_event - Create Weekly Recurring Event Until Date
**Priority:** P1  
**Type:** Functional  
**Tool:** `create_recurring_event`

#### Objective
Verify recurring event with end date works

#### Test Steps
1. Execute: `bunx fastmail create_recurring_event '{"title": "Weekly Review", "start": "2026-02-01T10:00:00", "end": "2026-02-01T11:00:00", "recurrence": "weekly", "recurrence_until": "2026-03-31"}'`

#### Expected Results
- Creates weekly events until specified end date

---

### TC-032: list_invitations - List Calendar Invitations
**Priority:** P2  
**Type:** Functional  
**Tool:** `list_invitations`

#### Objective
Verify pending calendar invitations are listed

#### Preconditions
- Account has at least 1 pending invitation

#### Test Steps
1. Execute: `bunx fastmail list_invitations`

#### Expected Results
- Returns array of invitation objects
- Each has: `eventId`, `calendarId`, `title`, `organizer`, `start`, `end`, `myStatus`

---

### TC-033: respond_to_invitation - Accept/Decline Invitation
**Priority:** P2  
**Type:** Functional  
**Tool:** `respond_to_invitation`

#### Objective
Verify invitation responses work

#### Preconditions
- TC-032 passed (have invitation event_id)

#### Test Steps
1. Execute: `bunx fastmail respond_to_invitation '{"event_id": "EVENT_ID", "response": "accept"}'`
2. Execute: Test decline with another invitation: `bunx fastmail respond_to_invitation '{"event_id": "EVENT_ID2", "response": "decline"}'`

#### Expected Results
- `success: true`
- Status updated in invitation list
- Organizer receives response notification

---

## Reminder Tools Test Cases

### TC-034: add_event_reminder - Add 15-Minute Reminder
**Priority:** P1  
**Type:** Functional  
**Tool:** `add_event_reminder`

#### Objective
Verify reminder can be added to existing event

#### Preconditions
- TC-024 passed (have event_id)

#### Test Steps
1. Execute: `bunx fastmail add_event_reminder '{"event_id": "EVENT_ID", "minutes_before": 15}'`

#### Expected Results
- `success: true`
- Reminder appears in list_event_reminders
- Returns `reminderId`

---

### TC-035: add_event_reminder - Add Email Reminder 1 Day Before
**Priority:** P1  
**Type:** Functional  
**Tool:** `add_event_reminder`

#### Objective
Verify different reminder types and times work

#### Test Steps
1. Execute: `bunx fastmail add_event_reminder '{"event_id": "EVENT_ID", "days_before": 1, "action": "email", "description": "Don't forget!"}'`

#### Expected Results
- Reminder created with email action
- Custom description preserved

---

### TC-036: remove_event_reminder - Remove Specific Reminder
**Priority:** P1  
**Type:** Functional  
**Tool:** `remove_event_reminder`

#### Objective
Verify reminders can be removed individually or all at once

#### Preconditions
- TC-034 passed (have reminder_id)

#### Test Steps
1. Remove specific: `bunx fastmail remove_event_reminder '{"event_id": "EVENT_ID", "reminder_id": "REMINDER_ID"}'`
2. Remove all: `bunx fastmail remove_event_reminder '{"event_id": "EVENT_ID"}'`

#### Expected Results
- `success: true`
- `removedCount` reflects number removed

---

### TC-037: list_event_reminders - List All Reminders for Event
**Priority:** P1  
**Type:** Functional  
**Tool:** `list_event_reminders`

#### Objective
Verify all reminders for an event can be listed

#### Preconditions
- Event has at least 2 reminders (from TC-034, TC-035)

#### Test Steps
1. Execute: `bunx fastmail list_event_reminders '{"event_id": "EVENT_ID"}'`

#### Expected Results
- Returns array of reminder objects
- Each has: `id`, `minutesBefore`/`hoursBefore`/`daysBefore`, `action`, `description`
- `total` count accurate

---

### TC-038: create_event_with_reminder - Create Event with Multiple Reminders
**Priority:** P0  
**Type:** Functional  
**Tool:** `create_event_with_reminder`

#### Objective
Verify event can be created with reminders in one call

#### Test Steps
1. Execute: `bunx fastmail create_event_with_reminder '{"title": "Important Meeting", "start": "2026-02-25T10:00:00", "end": "2026-02-25T11:00:00", "reminder_minutes": [15, 60, 1440]}'`

#### Expected Results
- `success: true`
- Event created
- Returns `eventId` and `reminders` array
- All 3 reminders created (15 min, 1 hour, 1 day)

---

## Environment & Error Handling Test Cases

### TC-039: Missing API Token - Email Operation
**Priority:** P0  
**Type:** Negative  
**Area:** Authentication

#### Objective
Verify graceful error when FASTMAIL_API_TOKEN is missing

#### Test Steps
1. Unset: `unset FASTMAIL_API_TOKEN`
2. Execute: `bunx fastmail list_mailboxes`

#### Expected Results
- `success: false`
- Error message: "FASTMAIL_API_TOKEN environment variable is required"
- Exit code non-zero

---

### TC-040: Missing CalDAV Credentials - Calendar Operation
**Priority:** P0  
**Type:** Negative  
**Area:** Authentication

#### Objective
Verify graceful error when calendar credentials missing

#### Test Steps
1. Keep FASTMAIL_API_TOKEN set
2. Unset: `unset FASTMAIL_USERNAME FASTMAIL_PASSWORD`
3. Execute: `bunx fastmail list_calendars`

#### Expected Results
- `success: false`
- Error message about required environment variables

---

### TC-041: Invalid API Token
**Priority:** P0  
**Type:** Negative  
**Area:** Authentication

#### Objective
Verify proper error handling for invalid/expired token

#### Test Steps
1. Set invalid token: `export FASTMAIL_API_TOKEN="invalid_token_12345"`
2. Execute: `bunx fastmail list_mailboxes`

#### Expected Results
- `success: false`
- Error: "Failed to get session: 401 Unauthorized"
- Clear authentication failure message

---

### TC-042: Invalid CalDAV Password
**Priority:** P0  
**Type:** Negative  
**Area:** Authentication

#### Objective
Verify proper error for invalid app password

#### Test Steps
1. Set valid username but wrong password
2. Execute: `bunx fastmail list_calendars`

#### Expected Results
- `success: false`
- 401 Unauthorized error
- Suggests checking app password (not main password)

---

### TC-043: Timezone Auto-Detection
**Priority:** P1  
**Type:** Functional  
**Area:** Configuration

#### Objective
Verify system timezone is auto-detected

#### Test Steps
1. Ensure FASTMAIL_TIMEZONE is not set
2. Execute: `bunx fastmail list_events '{"start_date": "2026-01-01", "end_date": "2026-01-31"}'`
3. Verify times match system timezone

#### Expected Results
- Events displayed in system local timezone
- No errors

---

### TC-044: Timezone Override
**Priority:** P1  
**Type:** Functional  
**Area:** Configuration

#### Objective
Verify FASTMAIL_TIMEZONE overrides system timezone

#### Test Steps
1. Set: `export FASTMAIL_TIMEZONE="America/New_York"`
2. Create event at specific time
3. Verify event stored/retrieved in specified timezone

#### Expected Results
- Times shown in America/New_York timezone
- DST handled correctly if applicable

---

### TC-045: CLI Help Display
**Priority:** P2  
**Type:** Functional  
**Area:** CLI

#### Objective
Verify help text displays correctly

#### Test Steps
1. Execute: `bunx fastmail --help`

#### Expected Results
- Shows usage information
- Lists all available commands
- Shows environment variable requirements

---

### TC-046: CLI List Tools
**Priority:** P2  
**Type:** Functional  
**Area:** CLI

#### Objective
Verify tool list displays all 27 tools

#### Test Steps
1. Execute: `bunx fastmail --list`

#### Expected Results
- Lists all 27 tools
- Organized by category (Email, Bulk, Calendar, Reminder)
- Numbered correctly (1-27)

---

## Regression Suite (Critical Path)

### RS-001: Email Workflow (End-to-End)
**Priority:** P0

1. List mailboxes
2. List emails from inbox
3. Get email content
4. Reply to email
5. Move email to archive
6. Search for the moved email

**Expected:** Complete workflow succeeds without errors

---

### RS-002: Calendar Workflow (End-to-End)
**Priority:** P0

1. List calendars
2. Create event
3. Add reminder to event
4. Update event time
5. List events in range
6. Get event details
7. Delete event

**Expected:** Complete workflow succeeds without errors

---

### RS-003: Bulk Operations Smoke Test
**Priority:** P0

1. Create 5 test emails
2. Bulk move all to archive
3. Bulk mark all as read
4. Bulk delete all

**Expected:** All bulk operations succeed, correct counts returned

---

## Edge Cases to Consider

1. **Email edge cases:**
   - Very long subject lines (>255 chars)
   - Empty body
   - Special characters in email addresses
   - Unicode content (Thai, emoji, etc.)
   - Large number of recipients (>50)

2. **Calendar edge cases:**
   - Event spanning midnight
   - DST transition times
   - Very long recurring series (>1000 occurrences)
   - Event with many attendees (>100)
   - All-day event spanning multiple days

3. **Timezone edge cases:**
   - Events during DST transition
   - UTC timezone
   - Negative UTC offsets
   - Asia/Tokyo (no DST)

4. **Error edge cases:**
   - Network timeout
   - Malformed JSON input
   - Very large limit parameters
   - Invalid date formats

---

**Document Version:** 1.0  
**Created:** 2026-02-01  
**Last Updated:** 2026-02-01
