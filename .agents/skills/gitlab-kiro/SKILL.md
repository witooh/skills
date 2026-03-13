---
name: gitlab-kiro
description: >
  Interact with GitLab via the glab CLI. Supports three MR workflows — Read (summarize),
  Review (full code/security/QA review), and Fix (review + implement). Trigger whenever the
  user provides a GitLab MR URL or says anything like "อ่าน MR", "ดู MR", "check MR",
  "review MR", "ช่วย review MR นี้", "ตรวจ MR", "แก้ตาม MR", "fix MR", or just pastes a
  GitLab MR URL. Also supports listing MRs, viewing MR status, checking CI/CD pipelines,
  approving MRs, and other glab operations. Trigger on "check pipeline", "list open MRs",
  or any GitLab-related task. When the user wants to fix issues from a MR — e.g. "แก้ตาม MR นี้",
  "fix MR", "แก้ issue ตาม MR", "แก้ MR <url>", "แก้ตาม review" — run the MR Fix workflow
  (review then ask user to invoke /neo-team-kiro for implementation).
compatibility:
  environment: kiro-cli
  tools:
    - execute_bash
    - fs_read
    - use_subagent
metadata:
  version: "1.0"
---

# GitLab Skill (Kiro CLI)

Use the `glab` CLI to interact with GitLab. Supports three MR workflows (Read → Review → Fix) plus general glab operations.

## URL Parsing

When given a GitLab MR URL like `https://gitlab.com/group/subgroup/project/-/merge_requests/42`:

- **repo_ref**: strip `https://` and everything from `/-/` onward → `gitlab.com/group/subgroup/project`
- **mr_id**: extract the number after `merge_requests/` → `42`

These two values power most glab commands: `glab mr <cmd> <mr_id> --repo <repo_ref>`

## Intent Detection

When given a GitLab MR URL, determine the user's intent before selecting a workflow. There are three distinct workflows — **Read** is the lightest (just summarize), **Review** runs full specialist agents, and **Fix** reviews then implements changes. Default to Read when no strong signal indicates the user wants a full review or fix.

| Signal in User Request | Workflow |
|------------------------|----------|
| "อ่าน", "ดู", "check", "สรุป", "summary", bare URL with no action verb | **MR Read** — fetch MR info + diff, then summarize. No specialist agents. |
| "review", "ตรวจ", "ช่วย review", "review ให้หน่อย" | **MR Review** — full code/security/QA review via 3 parallel specialist agents, post findings as comment |
| "แก้", "fix", "แก้ตาม", "แก้ issue", "implement", "ทำตาม" | **MR Fix** — review first, then ask user to invoke /neo-team-kiro to implement fixes |

**Decision rule:**
1. If the user's message contains a fix/แก้ keyword → **MR Fix**
2. If the user's message explicitly says "review" or "ตรวจ" → **MR Review**
3. Everything else (bare URL, "อ่าน", "ดู", "check", "สรุป", or ambiguous) → **MR Read** (lightest option, no side effects)

---

## Specialist Reference Files

This skill delegates review work to three specialist agents. Their detailed instructions live in the neo-team-kiro skill's reference files. Before spawning review agents, read these files with `read`:

| Specialist | Reference File |
|------------|---------------|
| Code Reviewer | `.agents/skills/neo-team-kiro/references/code-reviewer.md` |
| Security | `.agents/skills/neo-team-kiro/references/security.md` |
| QA | `.agents/skills/neo-team-kiro/references/qa.md` |

---

## MR Read Workflow

The lightest workflow — no specialist agents, no comments posted. Just fetch MR data and present a concise summary to the user in the conversation.

```
1. Fetch MR info (JSON) and diff
2. Summarize in conversation
```

### Step 1: Fetch

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab mr diff <mr_id> --repo <repo_ref>
```

### Step 2: Summarize

Present a concise Thai summary covering:

- **MR metadata** — title, author, status, source → target branch, pipeline status
- **What changed** — brief description of the changes (group by area: features, refactoring, CI, docs, tests)
- **Files changed** — count and key files
- **Existing comments** — if there are review comments, briefly note them

Keep it terminal-friendly and scannable. Do NOT spawn specialist agents or post any comments on the MR.

---

## MR Review Workflow

When the user asks to review a MR (or intent is detected as "review"), run this pipeline:

```
1. Fetch MR info, diff, and existing comments
2. Read & summarize existing comments (understand what's already discussed)
3. code-reviewer + security + qa → review in PARALLEL (with comment context)
4. Compose Thai comment from template
5. Post comment to the MR
```

### Step 1: Fetch

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab mr diff <mr_id> --repo <repo_ref>
glab mr note list <mr_id> --repo <repo_ref>
```

Extract from the view output: MR title, source branch, target branch, author.

### Step 2: Read Existing Comments

Before diving into the review, read through all existing MR comments/notes fetched in Step 1. This gives crucial context — other reviewers may have already flagged issues, the author may have explained design decisions, or there may be ongoing discussions that affect how you should review. Summarize the key points:

- Issues already raised by other reviewers
- Author's explanations or decisions
- Unresolved discussions that need attention
- Resolved items (avoid duplicating feedback)

This prevents the review from repeating what's already been said and helps focus on gaps that haven't been addressed yet.

### Step 3: Parallel Review

Read the project's `CLAUDE.md` or project conventions file if available. Then read the three specialist reference files listed above, and spawn all three subagents at the same time — including a summary of existing comments so reviewers have full context:

```json
{
  "command": "InvokeSubagents",
  "content": {
    "subagents": [
      {
        "query": "# Role: Code Reviewer\n[paste full code-reviewer instructions from .agents/skills/neo-team-kiro/references/code-reviewer.md]\n\n---\n## Project Conventions\n[relevant sections from conventions file if available, else omit]\n\n---\n## Existing MR Comments\n[summary of existing comments from Step 2]\nDo NOT repeat issues that other reviewers have already flagged unless you have additional insight to add.\n\n---\n## Task\nReview the following MR diff for convention compliance.\n\nMR: !<mr_id> — <mr_title>\nBranch: <source> → <target>\n\n## Diff\n<full diff output>",
        "relevant_context": "Code review specialist"
      },
      {
        "query": "# Role: Security Reviewer\n[paste full security instructions from .agents/skills/neo-team-kiro/references/security.md]\n\n---\n## Existing MR Comments\n[summary of existing comments from Step 2]\nDo NOT repeat security concerns that have already been raised unless you have additional findings.\n\n---\n## Task\nSecurity review the following MR diff.\n\nMR: !<mr_id> — <mr_title>\nBranch: <source> → <target>\n\n## Diff\n<full diff output>",
        "relevant_context": "Security review specialist"
      },
      {
        "query": "# Role: QA Reviewer\n[paste full QA instructions from .agents/skills/neo-team-kiro/references/qa.md]\n\n---\n## Project Conventions\n[relevant sections from conventions file if available, else omit]\n\n---\n## Existing MR Comments\n[summary of existing comments from Step 2]\nDo NOT repeat QA concerns that have already been raised unless you have additional findings.\n\n---\n## Task\nQA review the following MR diff. Focus on:\n- Test coverage gaps (are new code paths tested?)\n- Missing edge case tests\n- Regression risks\n- Acceptance criteria validation (if available)\n\nMR: !<mr_id> — <mr_title>\nBranch: <source> → <target>\n\n## Diff\n<full diff output>",
        "relevant_context": "QA review specialist"
      }
    ]
  }
}
```

### Step 4: Compose Thai comment

Read [references/mr-review-template.md](references/mr-review-template.md) and fill in findings from all three agents (code-reviewer, security, qa).

### Step 5: Post

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<thai_comment>"
```

If `glab` is not authenticated or fails, output the review in the conversation instead and tell the user.

---

## MR Fix Workflow

When intent is detected as "fix" (user wants to fix issues from a MR), run review first then hand off to /neo-team-kiro for implementation.

```
1. Fetch MR info, diff, and existing comments          (same as MR Review Step 1)
2. Read & summarize existing comments                   (same as MR Review Step 2)
3. code-reviewer + security + qa → review in PARALLEL   (same as MR Review Step 3)
4. Compile findings into structured handoff context
5. Ask user to invoke /neo-team-kiro with compiled findings
6. Post summary comment on MR (after fix is done)
```

### Steps 1-3: Same as MR Review

Run the exact same fetch → read comments → parallel review pipeline. The only difference is what happens after.

**Important for MR Fix:** When composing the subagent prompts in Step 3, add this instruction to each agent:

> Categorize every finding with a severity level: **Blocker**, **Critical**, **Warning**, or **Info**. Format each finding as: `[Severity] file:line — description`. This structured output is required for the handoff to the fix pipeline.

### Step 4: Compile Findings for Handoff

After all three review subagents return, compile their findings into a structured context:

```
## MR Fix Context

**MR:** !<mr_id> — <mr_title>
**Branch:** <source_branch> → <target_branch>
**Repository:** <repo_ref>

### Review Findings

#### Code Review Findings
<code_reviewer_output — full findings with severity levels>

#### Security Findings
<security_output — full findings with severity levels>

#### QA Findings
<qa_output — full findings with severity levels>

### Severity Summary
| Level | Count |
|-------|-------|
| Blocker | X |
| Critical | X |
| Warning | X |
| Info | X |

### MR Diff
<full diff for reference>
```

Only proceed to Step 5 if there are **Blocker or Critical** findings. If all findings are Warning/Info only:
1. Post the review comment on the MR (using the MR Review template from Step 4-5 of the Review workflow)
2. Inform the user in the conversation: "ไม่พบ Blocker/Critical — findings ทั้งหมดเป็น Warning/Info เท่านั้น ไม่จำเป็นต้องแก้ไขเร่งด่วน"
3. **End the workflow here.** Do NOT proceed to fix. The user can manually request fixes if desired.

### Step 5: Ask User to Invoke /neo-team-kiro

Since Kiro CLI does not have programmatic skill invocation, ask the user to load the neo-team-kiro skill:

```
กรุณาเรียก /neo-team-kiro แล้ว paste context ด้านล่างนี้:

แก้ไขโค้ดตาม review findings จาก MR

<compiled findings from Step 4>

## Instructions
- Fix all Blocker and Critical findings
- Address Warning findings where practical
- Info findings are optional improvements
- The MR diff is provided for context — the code is already in the working directory
- After fixing, run existing tests to verify nothing is broken
```

/neo-team-kiro will classify this as a **Bug Fix** workflow internally and run:
1. system-analyzer → understand the codebase + findings
2. developer + qa + code-reviewer → implement fixes + test + verify (3-WAY PARALLEL)
3. Remediation if needed

### Step 6: Post Summary Comment

After /neo-team-kiro completes (user will come back to this conversation), post a summary comment on the MR:

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<summary_comment>"
```

The comment should follow this format:

```
## 🤖 MR Fix Summary

**MR:** !<mr_id> — <mr_title>

### สิ่งที่แก้ไข
<list of fixes applied, mapped to original findings>

### สถานะ
- Blocker: X/Y แก้แล้ว
- Critical: X/Y แก้แล้ว
- Warning: X/Y แก้แล้ว

**ผลลัพธ์:** ✅ แก้ไขเสร็จ / ⚠️ แก้ไขบางส่วน (ดูรายละเอียดด้านบน)

---
*Fix โดย GitLab Skill + Neo Team · Kiro CLI*
```

---

## Common glab Operations

Use these directly via `shell` when the user asks for something other than a full review:

| Task | Command |
|------|---------|
| List open MRs | `glab mr list --repo <repo_ref>` |
| View MR details | `glab mr view <mr_id> --repo <repo_ref>` |
| Approve MR | `glab mr approve <mr_id> --repo <repo_ref>` |
| Check pipeline status | `glab ci status --repo <repo_ref>` |
| List pipelines | `glab ci list --repo <repo_ref>` |
| Retry a job | `glab ci retry <job_id> --repo <repo_ref>` |
| Add a note/comment | `glab mr note <mr_id> --repo <repo_ref> -m "<text>"` |

For `--repo`, you can omit it if you're already inside the project directory (glab detects the remote automatically).

## Error Handling

- **glab not authenticated**: tell the user to run `glab auth login`
- **glab command fails**: output the review as conversation text instead of posting, explain what failed
- **Empty diff**: note that the MR has no file changes and skip the review agents
- **Large diff (>500 lines)**: warn the user, proceed but note the review may miss details
