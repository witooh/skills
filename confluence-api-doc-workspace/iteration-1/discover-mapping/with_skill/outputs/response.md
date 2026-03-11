# Confluence API Doc Sync — Full Workflow Simulation

**Task inputs:**
- Confluence URL: `https://mycompany.atlassian.net`
- API doc file: `docs/api-doc.md`
- Email: `dev@mycompany.com`
- Parent page ID: `99887766`
- Page mapping: none (will use Option B — discover by title)

---

## Step 1: Gather Required Information

ข้อมูลที่ได้รับครบถ้วนแล้ว ยกเว้น **Atlassian API Token** ซึ่งในสถานการณ์จริงต้องขอจากผู้ใช้:

> กรุณาสร้าง API token ที่ https://id.atlassian.com/manage-profile/security/api-tokens
> แล้วแจ้ง token กลับมาเพื่อใช้ในการ sync

สำหรับ simulation นี้ สมมุติว่า token = `ATATT3xFf...` (placeholder)

---

## Step 2: Verify Authentication

คำสั่งตรวจสอบ acli authentication:

```bash
acli auth status
```

**Simulated output:**
```
Logged in as: dev@mycompany.com
Organization: mycompany.atlassian.net
Token status: valid
```

Authentication ผ่าน — ดำเนินการต่อได้

---

## Step 3: Read and Discover Sections

อ่านไฟล์ `docs/api-doc.md` และวิเคราะห์โครงสร้าง:

**Simulated file structure:**
```
## 1. Authentication
### 1.1 Login
### 1.2 Logout

## 2. User
### 2.1 Get Profile
```

**Section summary:**
```
Found 3 sections:
  Domain 1 - Authentication: 2 APIs (1.1 Login, 1.2 Logout)
  Domain 2 - User: 1 API (2.1 Get Profile)
```

ยืนยัน sync ทั้ง 3 sections

---

## Step 4: Map Sections to Confluence Page IDs

ผู้ใช้ไม่มี mapping อยู่แล้ว → ใช้ **Option B** ค้นหา children ของ parent page `99887766`

### คำสั่ง acli เพื่อ discover children:

```bash
acli confluence page view --id 99887766 --include-direct-children --json
```

**Simulated output:**
```json
{
  "id": "99887766",
  "title": "API Documentation",
  "children": [
    { "id": "11112222", "title": "1.1 Login" },
    { "id": "11113333", "title": "1.2 Logout" },
    { "id": "11114444", "title": "2.1 Get Profile" },
    { "id": "11115555", "title": "Changelog" }
  ]
}
```

### การ match section titles กับ child page titles:

| Section title (from api-doc.md) | Child page title match | Page ID  | Match result  |
|---------------------------------|------------------------|----------|---------------|
| 1.1 Login                       | 1.1 Login              | 11112222 | Matched       |
| 1.2 Logout                      | 1.2 Logout             | 11113333 | Matched       |
| 2.1 Get Profile                 | 2.1 Get Profile        | 11114444 | Matched       |

ทุก section match ได้ครบ — ไม่ต้องสร้างหน้าใหม่

**Final mapping:**
```
1.1 Login        → 11112222
1.2 Logout       → 11113333
2.1 Get Profile  → 11114444
```

---

## Step 5: Get Current Page Versions

ดึง version ปัจจุบันของแต่ละหน้าก่อน update:

```bash
acli confluence page view --id 11112222 --include-version --json
acli confluence page view --id 11113333 --include-version --json
acli confluence page view --id 11114444 --include-version --json
```

**Simulated output (per page):**
```json
{ "id": "11112222", "title": "1.1 Login",       "version": { "number": 3 } }
{ "id": "11113333", "title": "1.2 Logout",      "version": { "number": 1 } }
{ "id": "11114444", "title": "2.1 Get Profile", "version": { "number": 5 } }
```

**Version snapshot:**
```
1.1 Login        → CURRENT_VERSION=3
1.2 Logout       → CURRENT_VERSION=1
2.1 Get Profile  → CURRENT_VERSION=5
```

---

## Step 6: Convert Markdown to Confluence Storage Format

ตัวอย่างการแปลง section `1.1 Login` จาก Markdown เป็น Confluence Storage:

**Input Markdown:**
```markdown
### 1.1 Login

Authenticate and receive a JWT token.

**Endpoint:** `POST /auth/login`

**Request body:**
| Field    | Type   | Required |
|----------|--------|----------|
| email    | string | yes      |
| password | string | yes      |

**Example:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "secret"
}
\`\`\`
```

**Converted Confluence Storage Format:**
```xml
<h3>1.1 Login</h3>
<p>Authenticate and receive a JWT token.</p>
<p><strong>Endpoint:</strong> <code>POST /auth/login</code></p>
<p><strong>Request body:</strong></p>
<table><tbody>
  <tr><th>Field</th><th>Type</th><th>Required</th></tr>
  <tr><td>email</td><td>string</td><td>yes</td></tr>
  <tr><td>password</td><td>string</td><td>yes</td></tr>
</tbody></table>
<p><strong>Example:</strong></p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[{
  "email": "user@example.com",
  "password": "secret"
}]]></ac:plain-text-body>
</ac:structured-macro>
```

---

## Step 7: Update Existing Pages via REST API

### curl command template (generic):

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

### ตัวอย่าง curl ที่ใช้จริงสำหรับ `1.1 Login`:

```bash
curl -s -X PUT \
  "https://mycompany.atlassian.net/wiki/rest/api/content/11112222" \
  -u "dev@mycompany.com:ATATT3xFf..." \
  -H "Content-Type: application/json" \
  -d '{
    "version": {"number": 4},
    "title": "1.1 Login",
    "type": "page",
    "body": {
      "storage": {
        "value": "<h3>1.1 Login</h3><p>Authenticate and receive a JWT token.</p>...",
        "representation": "storage"
      }
    }
  }'
```

**Simulated HTTP responses:**
```
1.1 Login        → HTTP 200 OK  (updated)
1.2 Logout       → HTTP 200 OK  (updated)
2.1 Get Profile  → HTTP 200 OK  (content unchanged, skipped)
```

> หมายเหตุ: `2.1 Get Profile` ถูก skip เพราะ normalized content เหมือนกับที่มีอยู่ใน Confluence (ไม่มีการเปลี่ยนแปลง)

---

## Step 9: Result Summary

| Section         | Page ID  | Status               |
|-----------------|----------|----------------------|
| 1.1 Login       | 11112222 | Updated (v3 -> v4)   |
| 1.2 Logout      | 11113333 | Updated (v1 -> v2)   |
| 2.1 Get Profile | 11114444 | Skipped (no changes) |

**Total: 2 updated, 1 skipped, 0 created, 0 failed**

---

## Notes

- `acli` ใช้สำหรับ auth check และ read page version เท่านั้น
- Confluence REST API (`curl`) ใช้สำหรับ write/update operations
- Content comparison ช่วยลด version bump ที่ไม่จำเป็น
- ถ้า section ไหนไม่ match child page title จะต้องให้ผู้ใช้ระบุ page ID ด้วยตนเอง หรือใช้ Option C เพื่อสร้างหน้าใหม่
