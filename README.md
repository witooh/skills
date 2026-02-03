# Agent Skills

A collection of AI agent skills extending capabilities through specialized tools.

## Installation

```bash
npx skills add https://github.com/witooh/skills
```

## Communication & Productivity

| Skill                          | Tools | Description                               |
| ------------------------------ | ----- | ----------------------------------------- |
| [fastmail](./skills/fastmail/) | 27    | Fastmail email & calendar (JMAP + CalDAV) |

## Development & Automation

| Skill                              | Tools | Description                                          |
| ---------------------------------- | ----- | ---------------------------------------------------- |
| [agent-browser](./skills/agent-browser/) | 20+   | Browser automation for testing, screenshots, forms   |

## Finance & Markets

| Skill                                        | Tools | Description                                                              |
| -------------------------------------------- | ----- | ------------------------------------------------------------------------ |
| [dca-analyst](./skills/dca-analyst/)         | -     | DCA & eDCA portfolio analysis with technical indicators & market data    |
| [stock-market](./skills/stock-market/)       | 5     | Real-time stock & ETF prices (US, Thai SET, Crypto)                      |
| [sentiment-voter](./skills/sentiment-voter/) | 2     | Multi-LLM sentiment analysis for stocks/ETF/crypto with voting & caching |
| [coindesk-news](./skills/coindesk-news/)     | 3     | Cryptocurrency news from CoinDesk with sentiment filtering               |
| [massive-news](./skills/massive-news/)       | 1     | Stock & ETF news from Massive API with sentiment analysis                |

---

**Usage:** `bunx {skill-name} {tool} '{"param": "value"}'`
**Create:** Run `/skill-creator` first, see [AGENTS.md](./AGENTS.md)
**Spec:** https://agentskills.io/specification
