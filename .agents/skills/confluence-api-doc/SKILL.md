---
name: confluence-api-doc
description: Sync API documentation from a Markdown file to Confluence pages using acli + REST API. Prompts for Confluence URL, API doc file path, and credentials at runtime — no pre-configured environment variables required. Use this skill whenever: uploading or syncing API docs to Confluence, updating Confluence pages from a Markdown file, publishing documentation, "sync api doc", "push doc to confluence", "อัปเดต api doc ไป confluence", "sync confluence pages", "confluence-api-doc", or when the user wants to publish or update any Markdown-based documentation to Confluence.
---

# Confluence API Doc Sync

Sync API documentation sections from a Markdown file to Confluence pages. Uses `acli` for authentication verification and page reading (to get current version), and Confluence REST API via `curl` for page updates.

## Step 1: Gather Required Information

Ask the user for the following (if not already provided):

1. **API doc file path** — e.g., `docs/api-doc.md` (relative to project root, or absolute)
2. **Parent page URL** — the Confluence page under which API doc pages live (or will be created), e.g., `https://company.atlassian.net/wiki/spaces/PROJ/pages/123456789/API+Reference`

Extract the **page ID** directly from the URL (the numeric segment, e.g., `123456789`).

Do NOT ask for Confluence URL, email, or API token — those are resolved automatically in the next step.

## Step 2: Verify Authentication and Resolve Credentials

```bash
acli auth status
```

If not authenticated or acli not found:
- Not installed → tell user: `brew install atlassian/tap/acli` or visit https://developer.atlassian.com/cloud/acli/install/
- Not authenticated → guide user to run: `acli auth login`

From the output, extract:
- **CONFLUENCE_URL** — `Site:` field prefixed with `https://`, e.g., `company.atlassian.net` → `https://company.atlassian.net`
- **EMAIL** — `Email:` field, e.g., `user@company.com`

> **Why REST API for writes?** `acli confluence page` currently only supports `view`. For page create/update we use Confluence REST API via `curl`. URL and email come from `acli auth status`; only the API token needs to be resolved (at write time).

## Step 3: Read and Discover Sections

Read the API doc file and identify sections. Common pattern:

```
## 1. Authentication         ← domain group header
### 1.1 Login               ← individual API page (map to one Confluence page)
### 1.2 Refresh Token       ← individual API page
## 2. Consent               ← next domain group
### 2.1 Accept Consent      ← individual API page
```

After scanning, show the user a summary:
```
Found N sections:
  Domain 1: X APIs
  Domain 2: Y APIs
  ...
```

Ask the user to confirm or specify which sections to sync (all or specific ones).

## Step 4: Map Sections to Confluence Page IDs

Ask the user: "Do you have a page ID mapping already, or should I look up pages by title?"

**Option A — User provides mapping:** Accept a list like:
```
1.1 Login → 123456789
1.2 Refresh Token → 234567890
```

**Option B — Look up by title under a parent page:**
Ask for the parent page ID, then fetch its children and space key in one call:
```bash
curl -s "${CONFLUENCE_URL}/wiki/rest/api/content/${PARENT_PAGE_ID}?expand=space,children.page" \
  -u "${EMAIL}:${API_TOKEN}"
```
From the response extract:
- `space.key` → save as `SPACE_KEY` (needed if creating new pages)
- `children.page.results[]` → list of `{id, title}` to match against section titles

Match section titles to child page titles to build the `section → pageId` mapping automatically.

**Option C — Create new pages:**
For sections with no matching page, create them as children of a parent page via REST API (see Step 6 below).

## Step 5: Get Current Page Versions

For each page in the mapping, fetch its current version number (required for updates):

```bash
acli confluence page view --id <PAGE_ID> --include-version --json
```

Extract `version.number` from the JSON output. Store as `CURRENT_VERSION` per page.

## Step 6: Convert Markdown to Confluence Storage Format

For each section, convert the Markdown content to Confluence storage format (XHTML-based):

| Markdown | Confluence Storage |
|---|---|
| ` ```lang\ncode\n``` ` | `<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">lang</ac:parameter><ac:plain-text-body><![CDATA[code]]></ac:plain-text-body></ac:structured-macro>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `[text](url)` | `<a href="url">text</a>` |
| `## Heading` | `<h2>Heading</h2>` |
| `\| col \| col \|` table | `<table><tbody><tr><td>...</td></tr></tbody></table>` |

For `js`, `javascript`, `sh`, `bash`, `json`, `yaml` code blocks, map to the Confluence language name accordingly (`bash` for `sh`, `javascript` for `js`).

## Step 7: Update Existing Pages via REST API

Before writing, resolve the API token:

```bash
echo $CONFLUENCE_API_TOKEN
```

- If set → use it silently, no need to ask
- If empty → ask the user once:
  > "ต้องการ API token สำหรับ write ผ่าน Confluence REST API (acli ยังไม่ support page write) — generate ได้ที่ https://id.atlassian.com/manage-profile/security/api-tokens"

Use `EMAIL` extracted from `acli auth status` in Step 2.

For each section with an existing page ID:

```bash
curl -s -X PUT \
  "${CONFLUENCE_URL}/wiki/rest/api/content/${PAGE_ID}" \
  -u "${EMAIL}:${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"version\": {\"number\": $((CURRENT_VERSION + 1))},
    \"title\": \"${SECTION_TITLE}\",
    \"type\": \"page\",
    \"body\": {
      \"storage\": {
        \"value\": \"${ESCAPED_HTML}\",
        \"representation\": \"storage\"
      }
    }
  }"
```

Check HTTP status — 200 means success.

> **Content comparison tip:** Before updating, compare normalized content (collapse whitespace) to skip pages with no real changes. This avoids unnecessary version bumps.

## Step 8: Create New Pages via REST API

For sections with no existing page ID (Option C from Step 4):

```bash
curl -s -X POST \
  "${CONFLUENCE_URL}/wiki/rest/api/content" \
  -u "${EMAIL}:${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"type\": \"page\",
    \"title\": \"${SECTION_TITLE}\",
    \"ancestors\": [{\"id\": \"${PARENT_PAGE_ID}\"}],
    \"space\": {\"key\": \"${SPACE_KEY}\"},
    \"body\": {
      \"storage\": {
        \"value\": \"${ESCAPED_HTML}\",
        \"representation\": \"storage\"
      }
    }
  }"
```

Extract `id` from the response to save as the new page mapping.

## Step 9: Report Results

Print a summary table after all operations:

```
| Section               | Page ID    | Status                  |
|-----------------------|------------|-------------------------|
| 1.1 Login             | 123456789  | Updated (v3 → v4)       |
| 1.2 Refresh Token     | 234567890  | Skipped (no changes)    |
| 2.1 Accept Consent    | 345678901  | Created                 |
| 2.2 Reject Consent    | —          | Failed (HTTP 401)       |
```

Total: N updated, N skipped, N created, N failed.

## Error Reference

| Scenario | Action |
|---|---|
| `acli` not found | Install via `brew install atlassian/tap/acli` |
| `acli auth status` fails | Run `acli auth login` |
| API doc file not found | Re-ask for correct file path |
| HTTP 401 on REST call | Check API token — re-check `$CONFLUENCE_API_TOKEN` or ask user |
| HTTP 404 on page | Verify page ID is correct; page may have been deleted |
| HTTP 409 version conflict | Re-fetch version with acli and retry |
| Section title has no match | Ask user to manually provide page ID |
