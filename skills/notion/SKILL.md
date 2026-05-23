---
name: notion
description: >
  Interact with Notion workspaces via the `ntn` CLI tool (Notion's official CLI). Use this skill
  whenever the user wants to read, create, update, archive, or search Notion pages, query Notion
  databases (data sources), upload/list files, manage comments, or call any Notion REST endpoint
  from the terminal without opening a browser. Also trigger when the user says things like
  "ดู page Notion", "สร้าง page ใน Notion", "อัปเดต page", "query database Notion",
  "ค้นใน Notion", "อัปโหลดไฟล์ขึ้น Notion", "create notion page", "update notion db row",
  "search notion", "list notion users", or pastes a `notion.so` URL and wants to do something with
  it. Always run `ntn` via the shell execution tool — do not call the Notion REST API directly
  with `curl` when an `ntn` subcommand or `ntn api` invocation will do.
metadata:
  version: "1.0"
---

# Notion CLI (`ntn`) Skill

Use `ntn` to interact with Notion workspaces from the terminal. Reach for `ntn` whenever the user
asks about Notion — it handles auth, pagination, retries, and Markdown ↔ Notion-block conversion
for you, which raw `curl` against the REST API does not.

## Installation & version check

```bash
ntn --version                                # confirm installed
# Install if missing:
curl -fsSL https://ntn.dev | bash            # recommended (macOS / Linux, x64 + arm64)
# or
npm install --global ntn                     # requires Node 22+, npm 10+
```

Run `ntn doctor` if anything seems off (auth, network, version) — it's the diagnostic command.

## Authentication

```bash
ntn doctor                                   # check current auth / workspace
ntn login                                    # opens browser, stores token in OS keychain
ntn login --no-browser                       # headless: prints URL + code
ntn login poll                               # complete the headless flow
ntn logout                                   # clear credentials
```

Useful env vars (CI or scripted use):

| Var | Purpose |
|---|---|
| `NOTION_API_TOKEN` | Personal Access Token; overrides keychain |
| `NOTION_WORKSPACE_ID` | Pin a workspace when the token has access to several |
| `NOTION_KEYRING=0` | Store creds in a file instead of the OS keychain |
| `NOTION_API_VERSION` | Pin the Notion API version |

Guest / restricted members **cannot** log in — escalate to the workspace owner if you hit that.

---

## Core mental model

Notion exposes three layers, and the CLI mirrors them:

1. **Pages** — addressable by ID or URL. Content is editable as Markdown via `ntn pages`.
2. **Databases → Data sources → Rows.** A database is a container; the **data source** is the
   queryable table inside it. Rows are themselves pages. If the user gives you a database URL,
   resolve it to a data source ID before querying.
3. **Everything else** (blocks, users, comments, search, file uploads) lives behind `ntn api`,
   which is HTTPie-style.

Knowing this prevents the most common mistake: trying to `query` a database ID directly. You
must resolve it first.

---

## Pages

Pages are the primary unit. `ntn pages` round-trips Markdown, which is what you want 90% of the
time — it avoids the block-by-block API dance.

```bash
# View a page (returns Markdown)
ntn pages get <page-id-or-url>
ntn pages get <page-id-or-url> --json                  # raw API JSON instead

# Create a page from Markdown
ntn pages create --parent-page <parent-id> --title "Notes" --content-file notes.md
echo "# Hello" | ntn pages create --parent-page <parent-id> --title "Quick note"

# Update (append by default; use --replace to overwrite body)
ntn pages update <page-id> --content-file new.md
ntn pages update <page-id> --content-file new.md --replace

# Update properties only (no body change)
ntn pages update <page-id> --property Status=Done --property Priority:=2

# Move to trash (recoverable for 30 days from Notion UI)
ntn pages trash <page-id>
```

**Page IDs from URLs:** a URL like `https://www.notion.so/My-Page-abc123def456…` ends with the
ID. `ntn` accepts the full URL — no need to strip it.

---

## Databases & data sources

```bash
# Step 1: resolve database → data source ID(s)
ntn datasources resolve <database-id-or-url>

# Step 2: query the data source (NOT the database)
ntn api v1/data_sources/<ds-id>/query \
  filter:='{"property":"Status","select":{"equals":"Open"}}' \
  sorts:='[{"property":"Priority","direction":"descending"}]' \
  page_size:=50

# Or use the subcommand if you don't need advanced filtering:
ntn datasources query <ds-id> --filter '{"property":"Status","select":{"equals":"Open"}}'
```

**Hard limit:** `query` returns at most **10,000 rows** per data source. For larger sets, use
the Notion webhook/event stream — flag this to the user rather than silently truncating.

**Adding rows** (rows are pages whose parent is a data source):

```bash
ntn api v1/pages \
  parent[data_source_id]="<ds-id>" \
  properties[Name][title][0][text][content]="New task" \
  properties[Status][select][name]="Open" \
  properties[Priority][number]:=3
```

Note the HTTPie-style operators — see the **Body syntax cheat sheet** below.

---

## Search

```bash
# Search all pages/databases the integration can see
ntn api v1/search query==roadmap page_size==10

# Filter to only pages or only databases
ntn api v1/search query==roadmap filter[property]==object filter[value]==page
ntn api v1/search query==roadmap filter[property]==object filter[value]==database

# Sort newest first
ntn api v1/search sort[direction]==descending sort[timestamp]==last_edited_time
```

Search is workspace-scoped to whatever the authenticated integration/user can see. If results
look empty, check that the integration has been **shared** to the relevant pages — that's the
#1 cause of "but it's there in the UI" confusion.

---

## Files

```bash
# List uploaded files
ntn files list
ntn files list --json

# Upload a file (returns a file_upload ID you can attach to a property/block)
ntn files create --path ./screenshot.png
ntn files create --path ./report.pdf --name "Q4 Report.pdf"

# Get metadata for an upload
ntn files get <file-upload-id>
```

Attach an uploaded file to a page property:

```bash
ntn api "v1/pages/<page-id>" -X PATCH \
  properties[Attachment][files][0][type]=file_upload \
  properties[Attachment][files][0][file_upload][id]="<file-upload-id>" \
  properties[Attachment][files][0][name]="report.pdf"
```

---

## Comments, users, blocks (via `ntn api`)

These don't have dedicated subcommands — use `ntn api`:

```bash
# List users in the workspace
ntn api v1/users
ntn api v1/users/me                                    # bot/integration identity

# List comments on a page or block
ntn api v1/comments block_id==<page-or-block-id>

# Add a comment to a page
ntn api v1/comments \
  parent[page_id]="<page-id>" \
  rich_text[0][text][content]="Reviewed — looks good"

# List children blocks of a page (paginated)
ntn api "v1/blocks/<page-id>/children" page_size==100

# Append a block (e.g. a paragraph)
ntn api "v1/blocks/<page-id>/children" -X PATCH \
  children[0][object]=block \
  children[0][type]=paragraph \
  children[0][paragraph][rich_text][0][text][content]="Added via CLI"
```

For anything not covered here, run `ntn api ls` to see every endpoint, then
`ntn api <path> --spec` or `--docs` for inline schema help.

---

## Body syntax cheat sheet (HTTPie style)

`ntn api` uses HTTPie operators. Getting these right saves a lot of debugging:

| Operator | Meaning | Example |
|---|---|---|
| `key=value` | String body field | `properties[Name][title][0][text][content]="Hi"` |
| `key:=value` | JSON-typed body field (number/bool/array/object) | `archived:=true`, `properties[Score][number]:=5` |
| `key==value` | URL query string param | `page_size==50`, `query==roadmap` |
| `Header:value` | HTTP header | `Notion-Version:2022-06-28` |

POST is auto-inferred when body fields are present. Use `-X PATCH` / `-X DELETE` to override.
Pipe JSON in if a body gets unwieldy:

```bash
jq -n '{parent:{data_source_id:"<ds>"}, properties:{Name:{title:[{text:{content:"X"}}]}}}' \
  | ntn api v1/pages
```

---

## Practical workflows

### "What's on my Notion task DB?"

```bash
DB_URL="<paste url>"
DS_ID=$(ntn datasources resolve "$DB_URL" --json | jq -r '.[0].id')
ntn api "v1/data_sources/$DS_ID/query" \
  filter:='{"and":[
    {"property":"Status","select":{"does_not_equal":"Done"}},
    {"property":"Assignee","people":{"contains":"<user-id>"}}
  ]}' \
  sorts:='[{"property":"Due","direction":"ascending"}]' \
  --json | jq '.results[] | {title: .properties.Name.title[0].plain_text, due: .properties.Due.date.start}'
```

### "Save these meeting notes to Notion"

```bash
ntn pages create \
  --parent-page <notes-parent-id> \
  --title "Standup $(date +%Y-%m-%d)" \
  --content-file ./notes.md
```

### "Mark this task done and add a comment"

```bash
ntn pages update <task-id> --property Status=Done
ntn api v1/comments \
  parent[page_id]="<task-id>" \
  rich_text[0][text][content]="Closed via CLI — see commit abc123"
```

### "Find all unfinished pages mentioning 'migration'"

```bash
ntn api v1/search query==migration filter[property]==object filter[value]==page --json \
  | jq '.results[] | select(.archived == false) | {id, title: .properties.title.title[0].plain_text}'
```

---

## Output & scripting tips

- Default output: `ntn pages get` → **Markdown**, `ntn api` → **JSON**.
- Add `--json` to subcommands when you need to pipe to `jq`.
- Add `--verbose` to see HTTP status and headers (Authorization is redacted).
- `ntn api ls` lists every endpoint the CLI knows; pair with `--spec` for schemas.
- When the user gives you a Notion URL, you can pass it directly — `ntn` extracts the ID.
- When something fails with a permissions error, the integration is almost certainly not
  shared to that page/database. Say so explicitly so the user can fix it in the UI.

## When NOT to use this skill

- The user wants to embed a Notion view in a webpage — that's a Notion UI / share-link task, not
  a CLI task.
- The user wants to **build** a TypeScript app that runs inside Notion (`ntn workers …`) —
  that's outside the scope of this skill; point them at the Notion CLI docs directly.
- The user is hitting Notion via a different SDK in their codebase (e.g. `@notionhq/client`) —
  prefer their existing pattern over introducing `ntn`.
