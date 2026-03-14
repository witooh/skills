# Pipeline Completion Guard

Before declaring a task complete, verify ALL pipeline steps have been executed. This is a hard requirement — not optional.

## Checklist (run mentally before writing Summary)

```
For every workflow that includes code changes:
  ✅ Developer has completed implementation?
  ✅ QA has been invoked? (MANDATORY if QA is listed in the workflow definition)
  ✅ Code Reviewer has been invoked? (MANDATORY if Code Reviewer is listed in the workflow definition)
  ✅ Security has been invoked? (MANDATORY if Security is listed in the workflow definition)
  ✅ Remediation loop ran? (if any verification agent returned blocking findings)
  ✅ All blocking findings resolved or escalated to user?

  --- E2E Verification Gate (after QA returns) ---
  ✅ QA output contains "E2E Test Execution" section?
  ✅ If QA reports "E2E tests found: Yes" → result is not "Failed"?
     → If E2E failed due to current changes → trigger Remediation (QA is Blocked)
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
Example: New Feature (Simple)
  [ ] Step 1: architect
  [ ] Step 2: developer + qa (parallel)
  [ ] Step 3: code-reviewer + security (parallel)  ← DON'T FORGET THIS
  [ ] Step 4: remediation (if needed)
```

Mark each step as you complete it. Only write the Summary when all steps are marked done.
