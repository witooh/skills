# Agent Skills

A collection of AI agent skills extending capabilities through specialized tools.

## Installation

```bash
npx skills add https://github.com/witooh/skills
```

## Communication & Productivity

| Skill | Tools | Description |
| --- | --- | --- |
| [fastmail](./.agents/skills/fastmail/) | 27 | Fastmail email & calendar via JMAP + CalDAV |

## Development & Automation

| Skill | Tools | Description |
| --- | --- | --- |
| [agent-browser](./.agents/skills/agent-browser/) | - | Browser automation via Playwright for testing & data extraction |
| [brainstorm](./.agents/skills/brainstorm/) | 2 | Structured discovery & prompt improvement |
| [improve](./.agents/skills/improve/) | 1 | Iterative improvement until measurable criteria are met |
| [confluence-api-doc](./.agents/skills/confluence-api-doc/) | - | Sync API documentation from Markdown to Confluence pages via acli + REST API |
| [skill-creator](./.agents/skills/skill-creator/) | - | Meta-skill for creating and managing skills |

## Team Orchestration (multi-platform)

| Skill | Platform | Description |
| --- | --- | --- |
| [neo-team-claude](./.agents/skills/neo-team-claude/) | Claude Code | Orchestrate specialized dev agent team (model selection supported) |
| [neo-team-copilot](./.agents/skills/neo-team-copilot/) | Copilot CLI | Orchestrate specialized dev agent team (model selection supported) |
| [neo-team-kiro](./.agents/skills/neo-team-kiro/) | Kiro CLI | Orchestrate specialized dev agent team (default model only) |

## GitLab Integration (multi-platform)

| Skill | Platform | Description |
| --- | --- | --- |
| [gitlab-claude](./.agents/skills/gitlab-claude/) | Claude Code | GitLab MR Read/Review/Fix workflows via glab CLI |
| [gitlab-copilot](./.agents/skills/gitlab-copilot/) | Copilot CLI | GitLab MR Read/Review/Fix workflows via glab CLI |
| [gitlab-kiro](./.agents/skills/gitlab-kiro/) | Kiro CLI | GitLab MR Read/Review/Fix workflows via glab CLI |

## DevOps & Infrastructure

| Skill | Tools | Description |
| --- | --- | --- |
| [atlassian](./.agents/skills/atlassian/) | - | Jira & Confluence management via acli CLI |

## Health & Wellness

| Skill | Tools | Description |
| --- | --- | --- |
| [food-tracker](./.agents/skills/food-tracker/) | 1 | Phosphorus & potassium intake tracking for kidney health |

---

**Skills:** 14 total | **Tests:** [fastmail](./tests/fastmail/)
**Usage:** `cd .agents/skills/{skill-name} && bun scripts/cli.ts {tool} '{"param": "value"}'`
**Create:** Run `/skill-creator` first, see [CLAUDE.md](./CLAUDE.md)
**Spec:** https://agentskills.io/specification
