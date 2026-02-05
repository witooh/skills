# Regression Test Suite: Fastmail Skill

## Overview

**Purpose:** Critical path tests for Fastmail skill releases
**Duration:** 15-30 minutes
**Frequency:** Before each release, after major changes
**Total Tests:** 15

---

## Smoke Tests (Must Pass)

### Smoke-01: Environment Validation

**Purpose:** Verify all credentials are valid before testing

```bash
# Test Email API
export FASTMAIL_API_TOKEN="your-token"
bun scripts/cli.ts list_mailboxes

# Test Calendar API
export FASTMAIL_USERNAME="your-email@fastmail.com"
export FASTMAIL_PASSWORD="your-app-password"
bun scripts/cli.ts list_calendars
```

**Pass Criteria:**

- Both commands return `success: true`
- No authentication errors
- Response contains expected data structure

**Fail Action:** STOP - Fix credentials before proceeding

---

### Smoke-02: CLI Basic Operations

**Purpose:** Verify CLI interface works

```bash
bun scripts/cli.ts --help
bun scripts/cli.ts --list
```

**Pass Criteria:**

- Help displays usage information
- Tool list shows all 27 tools
- No errors or crashes

---

## Critical Path Tests

### CP-01: Email Read Workflow

**Priority:** P0
**Estimated Time:** 3 minutes

**Steps:**

1. List mailboxes → Get Inbox ID
2. List emails from Inbox (limit: 10)
3. Get full content of first email
4. Search emails with query from subject

**Verification:**

- All 4 operations succeed
- Data flows correctly between steps
- Email IDs are valid

---

### CP-02: Email Write Workflow

**Priority:** P0
**Estimated Time:** 5 minutes

**Steps:**

1. Send test email to self
2. List emails to find the sent email
3. Reply to the email
4. Set email as read
5. Move email to Archive

**Verification:**

- Email sends successfully with ID returned
- Reply sends with correct subject prefix
- Read status changes
- Move operation succeeds

---

### CP-03: Bulk Email Operations

**Priority:** P0
**Estimated Time:** 3 minutes

**Steps:**

1. Send 3 test emails to self
2. Get IDs from list_emails
3. Bulk move all 3 to Archive
4. Bulk set all as read
5. Bulk delete all 3

**Verification:**

- All bulk operations succeed
- `succeeded` array contains all 3 IDs
- `failed` array is empty
- Emails properly moved/deleted

---

### CP-04: Calendar Read Workflow

**Priority:** P0
**Estimated Time:** 2 minutes

**Steps:**

1. List calendars → Get calendar IDs
2. List events for next 7 days
3. Get details of first event (if any)
4. Search events with keyword

**Verification:**

- Calendar list returns valid data
- Events list returns array
- Event details has all required fields
- Search returns results (or empty if no matches)

---

### CP-05: Calendar Write Workflow

**Priority:** P0
**Estimated Time:** 5 minutes

**Steps:**

1. Create test event (today + 1 day, 1 hour duration)
2. Add 15-minute reminder
3. Update event title
4. List events to verify
5. Delete the event

**Verification:**

- Event created with ID
- Reminder added successfully
- Update persists
- Event appears in list
- Delete removes event completely

---

### CP-06: Recurring Event Creation

**Priority:** P1
**Estimated Time:** 2 minutes

**Steps:**

1. Create daily recurring event for 3 days
2. List events to verify 3 instances
3. Delete the recurring series

**Verification:**

- Recurring event created
- All 3 instances appear
- Deletion removes entire series

---

### CP-07: Reminder Management

**Priority:** P1
**Estimated Time:** 3 minutes

**Steps:**

1. Create event with 2 reminders (15 min, 1 hour)
2. List reminders
3. Add third reminder (1 day before, email action)
4. List reminders again (should be 3)
5. Remove all reminders
6. Delete event

**Verification:**

- Event created with reminders
- List shows correct count
- Add succeeds
- Remove clears all reminders

---

## Error Handling Tests

### EH-01: Missing Authentication

**Priority:** P0
**Estimated Time:** 1 minute

**Steps:**

1. Unset all environment variables
2. Try list_mailboxes → Should fail gracefully
3. Try list_calendars → Should fail gracefully

**Verification:**

- `success: false` for both
- Clear error messages about missing env vars
- No crashes or stack traces

---

### EH-02: Invalid Authentication

**Priority:** P0
**Estimated Time:** 1 minute

**Steps:**

1. Set invalid API token
2. Try list_mailboxes
3. Set valid token but invalid password
4. Try list_calendars

**Verification:**

- Both return 401 Unauthorized
- Error messages are helpful
- Suggests token/password verification

---

### EH-03: Invalid Parameters

**Priority:** P1
**Estimated Time:** 2 minutes

**Steps:**

1. Try get_email without email_id
2. Try send_email without required fields
3. Try create_event with invalid date format

**Verification:**

- All return `success: false`
- Validation errors are specific
- Required fields are identified

---

## Integration Tests

### INT-01: Email-to-Calendar Integration

**Priority:** P1
**Estimated Time:** 3 minutes

**Scenario:** Create calendar event from email

**Steps:**

1. Get email about meeting
2. Extract meeting details (time, location)
3. Create calendar event with those details
4. Add reminder

**Verification:**

- Both email and calendar operations succeed
- Data extracted correctly
- Event created with proper details

---

### INT-02: Thread Management

**Priority:** P2
**Estimated Time:** 2 minutes

**Steps:**

1. Get thread ID from an email
2. Get full thread
3. Reply to thread
4. Verify reply in thread

**Verification:**

- Thread contains all messages
- Reply appears in thread
- Participants list accurate

---

## Pass/Fail Criteria

### PASS (Release Ready):

- All Smoke tests pass
- 100% of CP (Critical Path) tests pass
- 80%+ of EH (Error Handling) tests pass
- 70%+ of INT (Integration) tests pass
- No data loss or corruption
- No security vulnerabilities

### FAIL (Block Release):

- Any Smoke test fails
- Any CP test fails
- Authentication bypass or security issue
- Data loss in bulk operations
- Crash or unhandled exception

### CONDITIONAL (Known Issues):

- P2 test failures with documented workarounds
- UI/UX issues (not functional)
- Minor error message improvements needed

---

## Execution Order

```
1. Smoke Tests (STOP if any fail)
2. Critical Path Tests (Must all pass)
3. Error Handling Tests (Validate robustness)
4. Integration Tests (Verify flows)
```

---

## Quick Regression Checklist

Before each release, verify:

- [ ] Smoke-01: Credentials valid
- [ ] Smoke-02: CLI works
- [ ] CP-01: Email read workflow
- [ ] CP-02: Email write workflow
- [ ] CP-03: Bulk operations
- [ ] CP-04: Calendar read workflow
- [ ] CP-05: Calendar write workflow
- [ ] CP-06: Recurring events
- [ ] CP-07: Reminder management
- [ ] EH-01: Missing auth handled
- [ ] EH-02: Invalid auth handled
- [ ] EH-03: Invalid params handled
- [ ] INT-01: Email-to-calendar flow
- [ ] INT-02: Thread management

**Regression Lead:** ********\_********
**Date:** ********\_********
**Result:** ☐ PASS ☐ FAIL ☐ CONDITIONAL

---

## Test Data Cleanup

After regression testing:

1. Delete all test emails created
2. Delete all test events created
3. Remove test labels/keywords
4. Verify test account is clean

---

## Version History

| Version | Date       | Changes                  | Tester          |
| ------- | ---------- | ------------------------ | --------------- |
| 1.0     | 2026-02-01 | Initial regression suite | QA Test Planner |

---

**Next Review:** Before v2.2 release
