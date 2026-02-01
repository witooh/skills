# Test Plan: Fastmail Skill

## Executive Summary

**Product:** Fastmail Email & Calendar Management Skill  
**Version:** 2.1  
**Test Plan ID:** TP-FASTMAIL-001  
**Total Tools:** 27 (10 Email + 3 Bulk + 10 Calendar + 4 Reminders)  
**Estimated Testing Time:** 4-6 hours  
**Priority:** High (Core Communication Infrastructure)

## Test Scope

### In Scope
- **Email Management (13 tools)**
  - Mailbox operations (list, organize)
  - Email CRUD (list, get, search, send, reply)
  - Email organization (move, labels, delete)
  - Thread management
  - Bulk operations (move, set labels, delete)

- **Calendar Management (14 tools)**
  - Calendar discovery (list calendars)
  - Event CRUD (list, get, create, update, delete)
  - Event search
  - Recurring events
  - Invitations (list, respond)
  - Reminders (add, remove, list, create with)

- **Environment & Configuration**
  - Environment variables validation
  - Timezone handling
  - Error handling & validation
  - Authentication flows

### Out of Scope
- Attachment handling (not implemented)
- Contact management (not implemented)
- JMAP Calendar (not available from Fastmail)
- Performance/load testing
- Security penetration testing

## Test Strategy

### Test Types
| Type | Coverage | Tools |
|------|----------|-------|
| **Functional** | 100% | All 27 tools with valid inputs |
| **Negative** | High | Invalid parameters, missing env vars, edge cases |
| **Integration** | Medium | End-to-end flows (create → update → delete) |
| **Error Handling** | High | Network failures, auth errors, validation |
| **Regression** | Critical | Bulk operations, recurring events, reminders |

### Test Approach
- **Black box testing** for CLI interface
- **API-level testing** for JMAP/CalDAV clients
- **Boundary value analysis** for date ranges, limits
- **Equivalence partitioning** for valid/invalid inputs

## Test Environment

### Requirements
- **Runtime:** Bun (JavaScript/TypeScript)
- **Dependencies:** @modelcontextprotocol/sdk, tsdav, uuid
- **OS:** macOS, Linux, Windows (cross-platform)

### Environment Variables Required
```bash
# For Email (JMAP)
export FASTMAIL_API_TOKEN="your-api-token"

# For Calendar (CalDAV)
export FASTMAIL_USERNAME="your-email@fastmail.com"
export FASTMAIL_PASSWORD="your-app-password"

# Optional
export FASTMAIL_TIMEZONE="Asia/Bangkok"  # or system default
```

### Test Data Setup
- **Test Email Account:** dedicated Fastmail account for testing
- **Test Emails:** Pre-populated inbox with various types (read/unread, attachments, threads)
- **Test Calendars:** Personal, Work calendars with sample events
- **Test Timezones:** UTC, America/New_York, Asia/Bangkok, Europe/London

---

## Entry & Exit Criteria

### Entry Criteria
- [ ] All environment variables configured
- [ ] Fastmail API token valid
- [ ] CalDAV credentials valid
- [ ] Test account has sample data
- [ ] Dependencies installed (`bun install`)

### Exit Criteria
- [ ] 100% of P0 tests passed
- [ ] 90%+ of P1 tests passed
- [ ] No critical bugs open
- [ ] All auth/security tests passed
- [ ] Bulk operation tests passed
- [ ] Error handling validated

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API token expires mid-test | Low | High | Pre-test token validation, backup token ready |
| Rate limiting from Fastmail | Medium | Medium | Add delays between tests, use test account |
| Timezone DST edge cases | Medium | Medium | Test multiple timezones, verify DST transitions |
| Bulk operation data loss | Low | Critical | Use isolated test account, backup before bulk ops |
| Network instability | Medium | Low | Retry logic tests, graceful error handling |

---

## Test Deliverables

1. **Test Plan Document** (this file)
2. **Test Cases** (detailed step-by-step)
3. **Test Execution Report** with results
4. **Bug Reports** (if any found)
5. **Regression Suite** for future releases

---

## Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| **Setup** | 30 min | Configure env, validate credentials, prep test data |
| **Email Tests** | 90 min | All 13 email tools (individual + bulk) |
| **Calendar Tests** | 90 min | All 10 calendar tools |
| **Reminder Tests** | 45 min | All 4 reminder tools |
| **Integration Tests** | 45 min | End-to-end flows |
| **Regression** | 30 min | Smoke tests, critical paths |
| **Reporting** | 30 min | Document results, file bugs |

**Total:** ~6 hours

---

## Tool Coverage Matrix

### Email Tools (13 total)

| Tool | Priority | Test Cases | Status |
|------|----------|------------|--------|
| `list_mailboxes` | P0 | TC-001 | Not Run |
| `list_emails` | P0 | TC-002, TC-003 | Not Run |
| `get_email` | P0 | TC-004 | Not Run |
| `get_thread` | P1 | TC-005 | Not Run |
| `search_emails` | P0 | TC-006, TC-007 | Not Run |
| `send_email` | P0 | TC-008, TC-009, TC-010 | Not Run |
| `reply_email` | P1 | TC-011, TC-012 | Not Run |
| `move_email` | P1 | TC-013 | Not Run |
| `set_labels` | P1 | TC-014, TC-015 | Not Run |
| `delete_email` | P1 | TC-016 | Not Run |
| `bulk_move_emails` | P1 | TC-017 | Not Run |
| `bulk_set_labels` | P2 | TC-018 | Not Run |
| `bulk_delete_emails` | P2 | TC-019 | Not Run |

### Calendar Tools (10 total)

| Tool | Priority | Test Cases | Status |
|------|----------|------------|--------|
| `list_calendars` | P0 | TC-020 | Not Run |
| `list_events` | P0 | TC-021, TC-022 | Not Run |
| `get_event` | P0 | TC-023 | Not Run |
| `create_event` | P0 | TC-024, TC-025, TC-026 | Not Run |
| `update_event` | P1 | TC-027 | Not Run |
| `delete_event` | P1 | TC-028 | Not Run |
| `search_events` | P1 | TC-029 | Not Run |
| `create_recurring_event` | P1 | TC-030, TC-031 | Not Run |
| `list_invitations` | P2 | TC-032 | Not Run |
| `respond_to_invitation` | P2 | TC-033 | Not Run |

### Reminder Tools (4 total)

| Tool | Priority | Test Cases | Status |
|------|----------|------------|--------|
| `add_event_reminder` | P1 | TC-034, TC-035 | Not Run |
| `remove_event_reminder` | P1 | TC-036 | Not Run |
| `list_event_reminders` | P1 | TC-037 | Not Run |
| `create_event_with_reminder` | P0 | TC-038 | Not Run |

### Environment & Error Handling

| Area | Priority | Test Cases | Status |
|------|----------|------------|--------|
| Missing API Token | P0 | TC-039 | Not Run |
| Missing CalDAV Credentials | P0 | TC-040 | Not Run |
| Invalid Token | P0 | TC-041 | Not Run |
| Invalid Credentials | P0 | TC-042 | Not Run |
| Timezone Handling | P1 | TC-043, TC-044 | Not Run |
| CLI Help/Version | P2 | TC-045, TC-046 | Not Run |

---

## Success Criteria

**PASS Requirements:**
- All P0 (Critical) tests: 100% pass
- All P1 (High) tests: 90%+ pass
- No critical bugs (data loss, security, crashes)
- All error handling graceful (no crashes, clear messages)
- Bulk operations complete successfully without data corruption
- Authentication properly validated

---

## Appendix

### A. Related Documentation
- [SKILL.md](../skills/fastmail/SKILL.md) - Skill overview
- [TOOLS.md](../skills/fastmail/references/TOOLS.md) - Detailed tool reference
- [README.md](../skills/fastmail/README.md) - Feature guide and troubleshooting
- [Fastmail API Docs](https://www.fastmail.com/dev/)
- [JMAP Specification](https://jmap.io/spec.html)
- [CalDAV RFC](https://datatracker.ietf.org/doc/html/rfc4791)

### B. Test Case Location
Detailed test cases: [./test_cases.md](./test_cases.md)

### C. Regression Suite
Regression tests: [./regression_suite.md](./regression_suite.md)

---

**Created:** 2026-02-01  
**Author:** QA Test Planner  
**Review Status:** Draft
