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

## Finance & Markets

| Skill | Tools | Description |
| --- | --- | --- |
| [massive-news](./.agents/skills/massive-news/) | 1 | Stock & ETF news from Massive API with sentiment analysis |

## Development & Automation

| Skill | Tools | Description |
| --- | --- | --- |
| [agent-browser](./.agents/skills/agent-browser/) | - | Browser automation via Playwright for testing & data extraction |
| [go-domain-generator](./.agents/skills/go-domain-generator/) | - | DDD + Clean Architecture Go code generation |
| [brainstorm](./.agents/skills/brainstorm/) | 2 | Structured discovery & prompt improvement |
| [loop](./.agents/skills/loop/) | 1 | Iterative improvement until measurable criteria are met |
| [neo-team](./.agents/skills/neo-team/) | 2 | Orchestrate specialized software development agent team |

## Health & Wellness

| Skill | Tools | Description |
| --- | --- | --- |
| [food-tracker](./.agents/skills/food-tracker/) | 1 | Phosphorus & potassium intake tracking for kidney health |

## DevOps & Infrastructure

| Skill | Tools | Description |
| --- | --- | --- |
| [consent-troubleshooting](./.agents/skills/consent-troubleshooting/) | 3 | AWS EKS + PostgreSQL consent service diagnostics |

---

**Skills:** 9 total | **Tests:** [fastmail](./tests/fastmail/), [massive-news](./tests/massive-news/)
**Usage:** `cd .agents/skills/{skill-name} && bun scripts/cli.ts {tool} '{"param": "value"}'`
**Create:** Run `/skill-creator` first, see [AGENTS.md](./AGENTS.md)
**Spec:** https://agentskills.io/specification
