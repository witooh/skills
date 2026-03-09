# Tools Reference

Detailed reference for configuring tools and MCP servers in custom agent profiles.

## Table of Contents
- [Tool Aliases](#tool-aliases)
- [Tool Configuration Patterns](#tool-configuration-patterns)
- [MCP Server Configuration](#mcp-server-configuration)
- [Out-of-the-box MCP Servers](#out-of-the-box-mcp-servers)

---

## Tool Aliases

All aliases are case-insensitive.

| Primary Alias | Compatible Aliases | Purpose |
|---|---|---|
| `execute` | `shell`, `Bash`, `powershell` | Run shell commands |
| `read` | `Read`, `NotebookRead` | Read file contents |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Create/modify files |
| `search` | `Grep`, `Glob` | Search files and text |
| `agent` | `custom-agent`, `Task` | Invoke another custom agent |
| `web` | `WebSearch`, `WebFetch` | Fetch URLs, web search |
| `todo` | `TodoWrite` | Manage task lists (VS Code only) |

## Tool Configuration Patterns

```yaml
# All tools (default — omit tools property)
---
name: unrestricted-agent
description: ...
---

# All tools explicitly
tools: ["*"]

# Read-only agent (safe for analysis/planning)
tools: ["read", "search"]

# Read + write, no execution
tools: ["read", "search", "edit"]

# Full development workflow
tools: ["read", "search", "edit", "execute"]

# No tools (analysis only via model knowledge)
tools: []
```

**Principle:** Grant the minimum tools needed. Read-only agents are safer for analysis tasks; add `execute` only when shell commands are genuinely required.

---

## MCP Server Configuration

Add MCP servers to extend agent capabilities:

```yaml
---
name: my-agent-with-mcp
description: Agent with custom MCP server
tools: ["read", "edit", "custom-mcp/my-tool"]
mcp-servers:
  custom-mcp:
    type: "local"          # or "stdio" (mapped to local)
    command: "npx"
    args: ["-y", "my-mcp-server"]
    env:
      API_KEY: ${{ secrets.COPILOT_MY_API_KEY }}
---
```

### Secret Syntax (all supported patterns)

```yaml
env:
  TOKEN: ${{ secrets.COPILOT_TOKEN }}     # recommended (Actions-style)
  TOKEN: ${{ var.COPILOT_TOKEN }}          # for variables
  TOKEN: $COPILOT_TOKEN                    # shell-style
  TOKEN: ${COPILOT_TOKEN}                  # Claude Code style
```

Secrets are sourced from the "copilot" environment in repository Settings → Environments.

### Scoping MCP Tools

```yaml
# All tools from a specific MCP server
tools: ["some-mcp/*"]

# Single tool from MCP server
tools: ["some-mcp/specific-tool"]

# Mix built-in and MCP tools
tools: ["read", "search", "my-mcp/query"]
```

---

## Out-of-the-box MCP Servers

These are available without configuration:

| MCP Server | Available Tools |
|---|---|
| `github` | All read-only GitHub tools (scoped to source repo). Use `github/*` or `github/<tool-name>` |
| `playwright` | Browser automation (localhost only). Use `playwright/*` or `playwright/<tool-name>` |

### Example: Agent using GitHub MCP

```yaml
---
name: pr-reviewer
description: Reviews pull requests for code quality issues
tools: ["read", "search", "github/list_pull_requests", "github/get_pull_request"]
---

You are a code reviewer. Analyze pull requests for bugs, security issues, and maintainability concerns.
Provide specific, actionable feedback with line references.
Do not approve or merge PRs—only provide review comments.
```