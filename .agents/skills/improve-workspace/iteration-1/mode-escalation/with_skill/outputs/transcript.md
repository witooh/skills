# Improve Skill Transcript

## Task

User request: "clean up this code" (`messy_handler.go` -- a Go HTTP handler for user CRUD)

---

## Mode Selection

**Initial assessment:** The phrase "clean up" is broad and touches multiple quality dimensions -- code duplication, naming conventions, idiomatic patterns, error handling consistency. This is NOT a single clear goal like "make this function faster".

**Decision: Quick Mode -> Escalated to Full Mode**

Rationale: "clean up" initially seems like it could be Quick Mode, but upon inspection the code has issues across multiple dimensions (DRY violations, non-idiomatic naming, inconsistent error handling, unused helpers). A single pass would either be superficial or try to change too many things without tracking. Escalating to Full Mode to get structured, measurable improvement.

**[Would ask user]:** "I see several cleanup opportunities -- duplicated response code, inconsistent naming, unused helper functions. Should I focus on just one area, or do a full structured cleanup across all of them?"

**Assumption:** User wants comprehensive cleanup. Proceeding with Full Mode.

---

## Step 1 -- Receive

Received: `messy_handler.go` -- a Go HTTP handler package with:
- `UserHandler` struct with CRUD methods (GetUser, CreateUser, UpdateUser, DeleteUser)
- `User` struct and `Database` interface
- Two helper functions (`writeJSON`, `writeError`) that exist but are NOT used by any handler

---

## Step 2 -- Establish Criteria

Based on the "clean up" request and Go code domain hints, I identified these criteria:

| Rank | Criterion | Specific Definition |
|------|-----------|---------------------|
| 1 | DRY (No duplicated logic) | Each distinct operation pattern exists exactly once; handlers call shared helpers |
| 2 | Idiomatic Go style | Follows Go conventions: `userID` not `userId`, `http.StatusXxx` constants, `any` not `interface{}`, proper error handling |
| 3 | Consistent error handling | All errors (including json.Marshal) are handled; error responses use the same mechanism everywhere |

**[Would ask user]:** "I suggest these 3 criteria ranked by impact. Do you agree, or would you reorder or replace any?"

**Assumption:** User agrees with these criteria and ranking.

---

## Step 3 -- Capture Baseline (Iteration 0)

Analyzing the original `messy_handler.go`:

### Issues Detected

**DRY violations:**
- ID parsing (query param -> int) is copy-pasted in GetUser, UpdateUser, DeleteUser (3x)
- JSON response writing (Marshal + Set header + WriteHeader + Write) is inlined in every handler (4x)
- Error response writing (WriteHeader + Write raw JSON string) is inlined ~9 times
- Helper functions `writeJSON` and `writeError` exist at bottom but are NEVER called

**Non-idiomatic Go:**
- Variable named `userId` instead of `userID` (Go convention: acronyms are all-caps)
- Uses magic numbers (400, 500, 200, 201, 204) instead of `http.StatusXxx` constants
- Uses `interface{}` instead of `any` (Go 1.18+)
- No constructor function for `UserHandler`
- `Database` interface defined after usage instead of before
- No doc comments on exported types/functions

**Inconsistent error handling:**
- `json.Marshal` errors silently ignored with `_` in all handlers
- Handlers use raw string JSON (`{"error": "..."}`) while `writeError` uses `fmt.Fprintf` (injection-prone if msg contains quotes)
- `writeJSON` also ignores marshal errors with `_`

### Iteration 0 -- Baseline Scorecard

| Criterion | Score | Evidence |
|-----------|-------|----------|
| DRY (No duplicated logic) | 0 | ID parsing duplicated 3x, response writing duplicated 4x, error responses duplicated ~9x. Helper functions exist but unused. |
| Idiomatic Go style | 0 | `userId` naming, magic status numbers, `interface{}`, no constructor, no doc comments, poor declaration order |
| Consistent error handling | 1 | Errors from db operations are logged and returned. However, json.Marshal errors are silently dropped, and `writeError` has a format-string injection risk. |

**Total: 1 / 6**
**Key gaps:** DRY violations (0) and non-idiomatic style (0) are the biggest gaps. Error handling is partially there but inconsistent.

---

## Step 4 -- Iteration 1: Eliminate DRY Violations (Largest Gap, Rank #1)

**Goal:** Extract duplicated patterns into shared helper functions and use them consistently.

**Changes made:**
1. Created `parseIDParam(w, r) (int, bool)` helper to extract and validate the `id` query parameter -- replaces 3 copies of the same 10-line block
2. Made all handlers call `writeJSON()` for success responses -- replaces 4 inline marshal+write blocks
3. Made all handlers call `writeError()` for error responses -- replaces ~9 inline error response blocks
4. Rewrote `writeError()` to call `writeJSON()` with a typed `errorResponse` struct -- eliminates format-string injection risk and ensures consistency

### Iteration 1 Scorecard

| Criterion | Previous | Current | Delta |
|-----------|----------|---------|-------|
| DRY (No duplicated logic) | 0 | 2 | +2 |
| Idiomatic Go style | 0 | 0 | 0 |
| Consistent error handling | 1 | 1 | 0 |

**Total: 3 / 6 (was: 1 / 6, delta: +2)**
**Remaining gaps:** Idiomatic style (0), error handling consistency (1)
**Next action:** Fix idiomatic Go style issues (rank #2, scored 0)

**[Would ask user]:** "DRY issues are resolved -- all handlers now use shared helpers. The code went from ~170 lines to ~150. Does this scoring look right to you?"

**Assumption:** User agrees.

---

## Step 5 -- Iteration 2: Idiomatic Go Style (Next Largest Gap, Rank #2)

**Goal:** Make the code follow standard Go conventions.

**Changes made:**
1. Renamed `userId` to `userID` throughout (Go acronym convention)
2. Replaced all magic status numbers with `http.StatusXxx` constants (StatusOK, StatusCreated, StatusBadRequest, StatusInternalServerError, StatusNoContent)
3. Changed `interface{}` to `any` in `writeJSON` signature
4. Added `NewUserHandler` constructor function
5. Reordered declarations: interface -> struct -> constructor -> methods -> helpers
6. Added doc comments on all exported types, functions, and methods
7. Removed unused `fmt` import (no longer needed since `writeError` uses struct marshalling)

### Iteration 2 Scorecard

| Criterion | Previous | Current | Delta |
|-----------|----------|---------|-------|
| DRY (No duplicated logic) | 2 | 2 | 0 |
| Idiomatic Go style | 0 | 2 | +2 |
| Consistent error handling | 1 | 1 | 0 |

**Total: 5 / 6 (was: 3 / 6, delta: +2)**
**Remaining gaps:** Error handling consistency (1)
**Next action:** Fix remaining error handling inconsistency

**[Would ask user]:** "Style is now idiomatic Go. Naming, constants, doc comments, declaration order all follow conventions. Agree with the scores?"

**Assumption:** User agrees.

---

## Step 6 -- Iteration 3: Consistent Error Handling (Final Gap)

**Goal:** Handle ALL errors consistently, including json.Marshal.

**Changes made:**
1. `writeJSON` now checks `json.Marshal` error -- logs it and returns 500 instead of silently writing empty/malformed response
2. `writeJSON` sets Content-Type header BEFORE checking for marshal errors so error responses also have correct content type
3. `writeError` now delegates to `writeJSON` with a typed struct, eliminating the `fmt.Fprintf` format-string injection vulnerability entirely

### Iteration 3 Scorecard

| Criterion | Previous | Current | Delta |
|-----------|----------|---------|-------|
| DRY (No duplicated logic) | 2 | 2 | 0 |
| Idiomatic Go style | 2 | 2 | 0 |
| Consistent error handling | 1 | 2 | +1 |

**Total: 6 / 6 (was: 5 / 6, delta: +1)**
**Remaining gaps:** None
**Regression check:** No regressions detected. All previously-met criteria maintained.

**[Would ask user]:** "All three criteria are now fully met. The code handles all errors consistently, including marshal failures. Does this look complete to you?"

**Assumption:** User agrees.

---

## Step 7 -- Deliver

### Completion Condition

All criteria scored 2/2. Loop complete after 3 iterations.

### Final Output

See `improved.go` in this directory.

### Key Changes Summary

| Area | Before | After |
|------|--------|-------|
| ID parsing | Copy-pasted in 3 handlers (~30 lines) | Single `parseIDParam` helper (10 lines) |
| JSON responses | Inlined in every handler | All use `writeJSON` helper |
| Error responses | Raw string JSON with format-string risk | All use `writeError` -> `writeJSON` with typed struct |
| Naming | `userId`, magic numbers, `interface{}` | `userID`, `http.StatusXxx`, `any` |
| Marshal errors | Silently ignored with `_` | Logged and return 500 |
| Doc comments | None | All exported symbols documented |
| Constructor | None | `NewUserHandler(db)` provided |
| Line count | 171 lines | 156 lines (fewer lines despite adding comments) |

---

### Iteration History

| Iteration | Change | Total Score | Delta |
|-----------|--------|-------------|-------|
| 0 (Baseline) | -- | 1 / 6 | -- |
| 1 | Extract shared helpers, eliminate all duplicated response/error/ID-parsing code | 3 / 6 | +2 |
| 2 | Idiomatic Go: naming, constants, `any`, constructor, doc comments, declaration order | 5 / 6 | +2 |
| 3 | Consistent error handling: marshal errors checked, `writeError` uses typed struct | 6 / 6 | +1 |

**Final Score: 6 / 6**
**Criteria met:** DRY, Idiomatic Go style, Consistent error handling
**Criteria not met:** None

---

## Mode Escalation Notes

This task started as a potential Quick Mode candidate ("clean up" sounds simple), but escalated to Full Mode because:

1. The code had issues across 3 distinct quality dimensions
2. A single pass would have either been incomplete or made too many unrelated changes at once
3. Full Mode allowed tracking that each change improved a specific dimension without regressing others
4. The structured approach caught the `json.Marshal` silent error issue that a quick cleanup might have missed
