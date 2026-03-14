# Pipeline Completion Guard

Before declaring a task complete, verify ALL pipeline steps have been executed. This is a hard requirement — not optional.

## Checklist (run mentally before writing Summary)

```
For every workflow that includes code changes:
  ✅ Developer has completed implementation?
  ✅ Review Loop completed? (for New Feature, Bug Fix, and standalone Review Loop workflows)
     OR verification agents invoked? (for other workflows with inline verification)
  ✅ Code Reviewer has been invoked? (MANDATORY if listed in the workflow)
  ✅ Security has been invoked? (MANDATORY if listed in the workflow)
  ✅ QA has been invoked? (MANDATORY if listed in the workflow)
  ✅ Review loop ran? (if any verification agent returned blocking findings)
  ✅ All blocking findings resolved or escalated to user?

  --- E2E Verification Gate (after QA returns) ---
  ✅ QA output contains "E2E Test Execution" section?
  ✅ If QA reports "E2E tests found: Yes" → result is not "Failed"?
     → If E2E failed due to current changes → trigger review loop (QA is Blocked)
     → If E2E failed due to pre-existing issues → accept as Warning, note in Summary
  ✅ If QA reports "E2E tests found: No" → acceptable, no action needed

If ANY checkbox is ❌ → DO NOT write the Summary. Continue the pipeline.
```

## Common Mistake: Stopping After Developer

The most frequent pipeline failure is stopping after Developer returns successful output. Developer output feels like "the job is done" because the code is written — but **unreviewed code is unfinished work**.

After Developer completes, ALWAYS check: **what's the next step in this workflow?** If verification agents remain, delegate to them immediately in the same response.

## Pipeline Step Tracking

When starting a workflow, mentally track which steps remain:

```
Example: New Feature (Complex)
  [ ] Step 1: business-analyst
  [ ] Step 2: architect
  [ ] Step 3: Present plan (confirm with user)
  [ ] Step 4: developer
  [ ] Step 5: REVIEW LOOP (code-reviewer + security + qa loop)  ← DON'T FORGET THIS

Example: New Feature (Simple)
  [ ] Step 1: architect
  [ ] Step 2: developer
  [ ] Step 3: REVIEW LOOP (code-reviewer + security + qa loop)  ← DON'T FORGET THIS
```

Mark each step as you complete it. Only write the Summary when all steps are marked done.
