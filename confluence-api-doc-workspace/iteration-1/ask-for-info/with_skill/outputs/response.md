# Confluence API Doc Sync — ขั้นตอนการถามข้อมูล

ยินดีช่วยซิงค์ API doc ไปยัง Confluence ครับ ก่อนเริ่มต้องการข้อมูลดังนี้:

---

## คำถามที่ต้องถาม (Step 1: Gather Required Information)

ต้องการข้อมูล 4 อย่างต่อไปนี้ ถ้ายังไม่ได้ให้มาครับ:

**1. Confluence URL**
> URL ของ Confluence instance เช่น `https://company.atlassian.net`

**2. API doc file path**
> Path ของไฟล์ Markdown ที่ต้องการซิงค์ เช่น `docs/api-doc.md` (relative จาก project root หรือ absolute path)

**3. Atlassian email**
> อีเมลที่ใช้ login Atlassian (ใช้สำหรับ API token auth)

**4. Atlassian API token**
> API token สำหรับ REST API (สร้างได้ที่ https://id.atlassian.com/manage-profile/security/api-tokens)

---

## ลำดับการถาม

เนื่องจากผู้ใช้ยังไม่ได้ให้ข้อมูลใดเลย ควรถามพร้อมกันทีเดียวในข้อความเดียว เพื่อลดรอบการโต้ตอบ:

```
เพื่อซิงค์ API doc ไป Confluence ขอข้อมูลต่อไปนี้ครับ:

1. Confluence URL — เช่น https://company.atlassian.net
2. Path ของไฟล์ API doc (Markdown) — เช่น docs/api-doc.md
3. Atlassian email — อีเมลที่ใช้ login Atlassian
4. Atlassian API token — สร้างได้ที่ https://id.atlassian.com/manage-profile/security/api-tokens
```

---

## ขั้นตอนถัดไปหลังได้ข้อมูลครบ

| Step | Action |
|------|--------|
| Step 2 | Verify `acli` auth status |
| Step 3 | Read API doc file and discover sections |
| Step 4 | Map sections to Confluence page IDs (user provides, lookup by title, or create new) |
| Step 5 | Fetch current page versions for update operations |
| Step 6 | Convert Markdown to Confluence storage format (XHTML) |
| Step 7 | Update existing pages via REST API (`PUT`) |
| Step 8 | Create new pages via REST API (`POST`) if needed |
| Step 9 | Report results in summary table |

---

## หมายเหตุ

- ต้องการทั้ง `acli` (สำหรับ OAuth auth + อ่านข้อมูล page) และ API token (สำหรับ write/update ผ่าน REST API)
- ถ้ายังไม่มี `acli`: ติดตั้งด้วย `brew install atlassian/tap/acli`
- ถ้ายังไม่ได้ login: รัน `acli auth login`
