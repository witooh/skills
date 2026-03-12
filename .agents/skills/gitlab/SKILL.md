---
name: gitlab
description: Interact with GitLab via the glab CLI. Primary use case is MR review — fetches the diff, runs parallel code review + security review via specialist agents, then posts the result as a Thai comment on the MR. Also supports listing MRs, viewing MR status, checking CI/CD pipelines, approving MRs, and other glab operations. Trigger whenever the user provides a GitLab MR URL or says anything like "review MR", "ช่วย review MR นี้", "ดู MR ให้หน่อย", "review https://gitlab.../merge_requests/42", "check pipeline", "list open MRs", or any GitLab-related task.
---

# GitLab Skill

Use the `glab` CLI to interact with GitLab. The primary workflow is MR Review — but this skill handles any GitLab operation the user needs.

## URL Parsing

When given a GitLab MR URL like `https://gitlab.com/group/subgroup/project/-/merge_requests/42`:

- **repo_ref**: strip `https://` and everything from `/-/` onward → `gitlab.com/group/subgroup/project`
- **mr_id**: extract the number after `merge_requests/` → `42`

These two values power most glab commands: `glab mr <cmd> <mr_id> --repo <repo_ref>`

## MR Review Workflow

When the user asks to review a MR, run this pipeline:

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

Read the project's `CLAUDE.md` if available (for conventions). Then spawn all three agents at the same time, including a summary of existing comments so reviewers have full context:

```
Agent(
  description: "Code review MR diff",
  subagent_type: "code-reviewer",
  model: "opus",
  prompt: """
[code-reviewer agent instructions — read from ~/.claude/agents/code-reviewer.agent.md]

---
## Project Conventions
[relevant sections from CLAUDE.md if available, else omit]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat issues that other reviewers have already flagged unless you have additional insight to add.

---
## Task
Review the following MR diff for convention compliance.

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)

Agent(
  description: "Security review MR diff",
  subagent_type: "security",
  model: "sonnet",
  prompt: """
[security agent instructions — read from ~/.claude/agents/security.agent.md]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat security concerns that have already been raised unless you have additional findings.

---
## Task
Security review the following MR diff.

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)

Agent(
  description: "QA review MR diff",
  subagent_type: "qa",
  model: "sonnet",
  prompt: """
[qa agent instructions — read from ~/.claude/agents/qa.agent.md]

---
## Project Conventions
[relevant sections from CLAUDE.md if available, else omit]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat QA concerns that have already been raised unless you have additional findings.

---
## Task
QA review the following MR diff. Focus on:
- Test coverage gaps (are new code paths tested?)
- Missing edge case tests
- Regression risks
- Acceptance criteria validation (if available)

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)
```

Read the agent files from `~/.claude/agents/` before spawning, so the full agent instructions are included in the prompt.

### Step 4: Compose Thai comment

Read [references/mr-review-template.md](references/mr-review-template.md) and fill in findings from all three agents (code-reviewer, security, qa).

### Step 5: Post

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<thai_comment>"
```

If `glab` is not authenticated or fails, output the review in the conversation instead and tell the user.

---

## Common glab Operations

Use these directly via `Bash` when the user asks for something other than a full review:

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
