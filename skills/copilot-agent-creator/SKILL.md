---
name: copilot-agent-creator
description: Design and create GitHub Copilot custom agent profiles (.agent.md files) for the Copilot CLI and GitHub.com coding agent. Use when a user wants to create a new custom sub-agent, scaffold an agent profile, define agent expertise and instructions, configure tools or MCP servers, or improve an existing agent profile. Triggers on phrases like "create an agent", "new copilot agent", "make a sub-agent", "agent profile", ".agent.md", or "custom agent for copilot".
---

# Copilot Agent Creator

## Workflow

Creating a custom agent involves these steps:

1. **Clarify purpose** — understand expertise, scope, restrictions, and trigger conditions
2. **Choose location** — user-level (`~/.copilot/agents/`) or project-level (`.github/agents/`)
3. **Write the agent profile** — YAML frontmatter + markdown body
4. **Configure tools** — limit or expand tool access as needed
5. **Validate** — review description quality and instruction clarity

## Agent Profile Format

Every agent is a single `.agent.md` file:

```
<filename>.agent.md
├── YAML frontmatter  (name, description, tools, mcp-servers)
└── Markdown body     (behavior instructions, max 30,000 chars)
```

### YAML Frontmatter

```yaml
---
name: agent-display-name          # shown in /agent list
description: What it does + when to use it (trigger phrases, task types)
tools: ["read", "search", "edit"] # omit = all tools enabled
---
```

Only `name` and `description` are required. `description` is the primary trigger — make it specific about **when** the agent should be selected.

For full tools reference and MCP server config: see [references/tools-reference.md](references/tools-reference.md)

## File Locations

| Location | Path | Scope |
|---|---|---|
| **User-level** | `~/.copilot/agents/<name>.agent.md` | All repos on this machine |
| **Project-level** | `.github/agents/<name>.agent.md` | This repository only |

User-level takes precedence if names conflict.

## Writing Good Agent Instructions

The markdown body defines agent behavior. Structure it with:

- **Role statement** — who the agent is and its primary mission
- **Responsibilities** — bullet list of what it does
- **File/scope restrictions** — what it SHOULD and SHOULD NOT touch
- **Output expectations** — format, style, artifacts it creates
- **Clarification rules** — when to ask vs. act

### Example Agent Profile

```markdown
---
name: test-specialist
description: Writes and improves tests. Use when adding test coverage, fixing broken tests, reviewing test quality, or when phrases like "write tests", "test coverage", "unit test", or "add specs" appear.
tools: ["read", "search", "edit", "execute"]
---

You are a testing specialist focused on improving code quality through comprehensive testing.

**Responsibilities:**
- Analyze existing tests and identify coverage gaps
- Write unit, integration, and end-to-end tests following project conventions
- Fix broken or flaky tests
- Ensure tests are isolated, deterministic, and well-named

**Scope:**
- Work only in test files and test directories
- Do NOT modify production code unless a bug must be fixed to make a test pass
- Ask for clarification if production code changes seem necessary

**Output:**
- Follow the existing test framework and naming conventions in the project
- Include descriptive test names that explain the expected behavior
- Group related tests logically
```

## Agent Naming

- Use lowercase letters and hyphens only (e.g., `security-auditor`, `test-specialist`)
- The filename (minus `.agent.md`) is used for programmatic invocation: `copilot --agent security-auditor`
- `name` in frontmatter is the display name shown in menus

## Design Checklist

Before finishing an agent profile:

- [ ] `description` explains **what** the agent does AND **when** to use it (include trigger phrases)
- [ ] Markdown body has a clear role statement
- [ ] Scope restrictions are explicit (what it will/won't touch)
- [ ] Tools list matches the agent's actual needs (avoid giving more than necessary)
- [ ] Agent name is lowercase-hyphenated and reflects the role
