# Agent Skills Repository

Repository for creating and managing agent skills following the [Agent Skills Specification](https://agentskills.io/specification).

---

## Guardrails

### MUST DO

- [ ] **Always run `/skill-creator` before creating or modifying any skill**
- [ ] Follow the [Agent Skills Specification](https://agentskills.io/specification) strictly
- [ ] **Place skill in `./skills/<skill-name>/` directory**
- [ ] **Place test plan in `./tests/<skill-name>/` directory**
- [ ] Include valid YAML frontmatter with `name` and `description` in SKILL.md
- [ ] Test all scripts before packaging
- [ ] Use environment variables for secrets (never hardcode)
- [ ] Validate skill with `skills-ref validate` before release

### MUST NOT

- [ ] Create README.md, CHANGELOG.md, or other auxiliary docs (SKILL.md is the single source)
- [ ] Hardcode API keys, tokens, or passwords in code
- [ ] Use uppercase or underscores in skill names (use lowercase-hyphens only)
- [ ] Exceed 500 lines in SKILL.md (split to references/)
- [ ] Skip the `/skill-creator` skill when creating new skills
- [ ] Commit node_modules or .sisyphus directories

### PREFER

- [ ] Bun over Node.js for runtime
- [ ] TypeScript with strict mode
- [ ] ES Modules (`"type": "module"`)
- [ ] Progressive disclosure (metadata → SKILL.md → references)
- [ ] Consistent JSON output format with `success`, `data`, `timestamp`
- [ ] snake_case for tool names, kebab-case for file names

---

## Project Overview

This repository contains reusable skills that extend AI agent capabilities. Skills are modular packages providing specialized workflows, tool integrations, and domain expertise.

## Directory Structure

```
skills/
├── AGENTS.md                    # This file - project guidance
├── .gitignore                   # Git ignore rules
├── .opencode/                   # OpenCode framework configuration
│   ├── opencode.json           # OpenCode settings
│   └── package.json            # OpenCode plugin dependencies
│
└── skills/                      # All skills live here
    └── {skill-name}/           # Individual skill folder
        ├── SKILL.md            # Required - skill metadata + instructions
        ├── package.json        # Dependencies and CLI entry point
        ├── tsconfig.json       # TypeScript configuration
        ├── scripts/            # Executable code
        │   ├── cli.ts         # CLI entry point
        │   └── tools/         # Tool implementations
        └── references/         # Reference documentation
            └── TOOLS.md       # Detailed tool specifications
```

## Skill Format Specification

Every skill MUST follow the [Agent Skills Specification](https://agentskills.io/specification):

### Required Files

**SKILL.md** - The only required file containing:

1. **YAML Frontmatter** (required):

   ```yaml
   ---
   name: skill-name # Lowercase, hyphens only, 1-64 chars
   description: ... # What it does + when to use, 1-1024 chars
   compatibility: opencode # Optional: environment requirements
   metadata: # Optional: arbitrary key-value pairs
     author: your-name
     version: "1.0"
   ---
   ```

2. **Markdown Body** - Instructions and guidance for using the skill

### Optional Directories

| Directory     | Purpose                              | When to Include                    |
| ------------- | ------------------------------------ | ---------------------------------- |
| `scripts/`    | Executable code (TS, Python, Bash)   | Deterministic, reusable operations |
| `references/` | Documentation loaded on-demand       | Detailed specs, schemas, examples  |
| `assets/`     | Static resources (templates, images) | Files used in output               |

## Creating a New Skill

> **IMPORTANT:** Always load the `skill-creator` skill first when creating or updating skills:
>
> ```
> /skill-creator
> ```
>
> This skill provides comprehensive guidance on skill design patterns, progressive disclosure, and best practices.

### Step 1: Load skill-creator Skill

Before creating any skill, invoke the `skill-creator` skill for detailed guidance:

```
/skill-creator
```

The skill-creator provides:

- Core principles (concise context, degrees of freedom)
- Anatomy of a skill (SKILL.md structure, bundled resources)
- Progressive disclosure patterns
- Step-by-step creation process
- Design patterns for workflows and outputs

### Step 2: Create Skill Directory

```bash
mkdir -p skills/{skill-name}
```

### Step 3: Create SKILL.md

```markdown
---
name: my-skill
description: Brief description of what this skill does and when to use it. Include trigger keywords.
compatibility: opencode
metadata:
  author: your-name
  version: "1.0"
---

## Quick Start

[Minimal usage example]

## When to Use

- Condition 1
- Condition 2

## Tools

| Tool        | Purpose      |
| ----------- | ------------ |
| `tool_name` | What it does |

## Examples

[Common usage patterns]
```

### Step 4: Implement Scripts (if needed)

For TypeScript CLI tools:

```bash
# Create structure
mkdir -p skills/{skill-name}/scripts/tools

# package.json
{
  "name": "skill-name",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "skill-name": "./scripts/cli.ts"
  },
  "dependencies": {}
}

# tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "declaration": true,
    "outDir": "dist",
    "rootDir": "scripts"
  }
}
```

### Step 5: Add Reference Documentation

For complex skills, create `references/TOOLS.md` with detailed tool specifications.

### Step 6: Iterate Based on Usage

After testing, refine the skill based on real usage patterns. The `skill-creator` skill provides guidance on iteration workflows.

## Development Guidelines

### Naming Conventions

- **Skill names:** lowercase, hyphens only (e.g., `pdf-processor`, `email-client`)
- **Tool names:** snake_case (e.g., `send_email`, `create_event`)
- **File names:** kebab-case or snake_case

### Best Practices

1. **Keep SKILL.md concise** - Under 500 lines; move details to references/
2. **Description is critical** - Include what + when to use + trigger keywords
3. **Progressive disclosure** - Metadata (~100 tokens) → SKILL.md body (<5k tokens) → references (on-demand)
4. **Test scripts** - Always test executable scripts before packaging
5. **Environment variables** - Use for secrets, document in SKILL.md

### DO NOT Include

- README.md (SKILL.md serves this purpose)
- CHANGELOG.md
- INSTALLATION_GUIDE.md
- Any auxiliary documentation

### Output Format

All tool responses should return consistent JSON:

```json
{
  "success": true,
  "data": {
    /* tool-specific response */
  },
  "timestamp": "ISO-8601 timestamp"
}
```

## Technology Stack

- **Runtime:** [Bun](https://bun.sh/) (preferred) or Node.js
- **Language:** TypeScript (strict mode)
- **Module format:** ES Modules (`"type": "module"`)

## Environment Setup

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Install skill dependencies
cd skills/{skill-name}
bun install

# Run skill CLI
bunx {skill-name} --help
```

## Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) library to validate skills:

```bash
skills-ref validate ./skills/{skill-name}
```

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Full Documentation](https://agentskills.io/llms.txt)
- [JMAP Protocol](https://jmap.io/spec.html)
- [CalDAV RFC](https://datatracker.ietf.org/doc/html/rfc4791)

## Project Conventions

| Aspect             | Convention                                  |
| ------------------ | ------------------------------------------- |
| Runtime            | Bun (TypeScript)                            |
| Module             | ES Modules                                  |
| Timezone           | UTC+7 (Asia/Bangkok) default                |
| Languages          | English (Thai for specific skills)          |
| Config             | Environment variables for secrets           |
| Testing            | Manual validation before packaging          |
| **Skill Creation** | **Always use `/skill-creator` skill first** |

---

## Language Guidelines

**All documentation must be in English.** Thai is acceptable for:

- LLM/chat communication
- Specific skills targeting Thai-speaking users
