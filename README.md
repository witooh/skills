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
| [stock-market](./.agents/skills/stock-market/) | 5 | Real-time stock & ETF prices (US, Thai SET) |
| [coindesk-news](./.agents/skills/coindesk-news/) | 3 | Cryptocurrency news from CoinDesk with sentiment filtering |
| [massive-news](./.agents/skills/massive-news/) | 1 | Stock & ETF news from Massive API with sentiment analysis |
| [sentiment-voter](./.agents/skills/sentiment-voter/) | 2 | Multi-LLM sentiment analysis with voting & caching |
| [dca-analyst](./.agents/skills/dca-analyst/) | - | DCA & eDCA portfolio analysis with technical indicators |

## Development & Automation

| Skill | Tools | Description |
| --- | --- | --- |
| [agent-browser](./.agents/skills/agent-browser/) | - | Browser automation via Playwright for testing & data extraction |
| [copilot-agent-creator](./.agents/skills/copilot-agent-creator/) | - | Create custom GitHub Copilot agent profiles (.agent.md) |
| [go-domain-generator](./.agents/skills/go-domain-generator/) | - | DDD + Clean Architecture Go code generation |
| [brainstorm](./.agents/skills/brainstorm/) | - | Structured discovery & prompt improvement |

## Health & Wellness

| Skill | Tools | Description |
| --- | --- | --- |
| [food-tracker](./.agents/skills/food-tracker/) | 1 | Phosphorus & potassium intake tracking for kidney health |

## DevOps & Infrastructure

| Skill | Tools | Description |
| --- | --- | --- |
| [consent-troubleshooting](./.agents/skills/consent-troubleshooting/) | 3 | AWS EKS + PostgreSQL consent service diagnostics |

---

**Skills:** 12 total | **Tests:** [coindesk-news](./tests/coindesk-news/), [fastmail](./tests/fastmail/), [massive-news](./tests/massive-news/), [sentiment-voter](./tests/sentiment-voter/), [stock-market](./tests/stock-market/)
**Usage:** `cd .agents/skills/{skill-name} && bun scripts/cli.ts {tool} '{"param": "value"}'`
**Create:** Run `/skill-creator` first, see [AGENTS.md](./AGENTS.md)
**Spec:** https://agentskills.io/specification
