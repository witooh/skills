# GitLab MR Review — Reference

## Thai Comment Template

Use this template exactly when posting the review result via `glab mr note`:

```
## 🤖 ผลการ Review Merge Request โดย Neo Team

**MR:** !<mr_id> — <mr_title>
---

### 📋 Code Review

<code_reviewer_findings_in_thai>

---

### 🔒 Security Review

<security_findings_in_thai>

---

### สรุปผล

| ระดับ | จำนวน |
|-------|-------|
| Blocker | X |
| Critical | X |
| Warning | X |
| Info | X |

**ผลการตรวจสอบ:** ✅ Approved / ❌ ต้องแก้ไขก่อน Merge

<brief_next_steps_if_any_in_thai>

---
*Review โดย Neo Team · Claude Code*
```

## Translation Guide

Translate findings accurately into Thai. Keep file paths and code snippets in English.

| English          | Thai                |
| ---------------- | ------------------- |
| Blocker          | ต้องแก้ไข (บล็อก)   |
| Critical         | วิกฤต               |
| Warning          | คำเตือน             |
| Info             | ข้อเสนอแนะ          |
| Approved         | อนุมัติ             |
| Changes Required | ต้องแก้ไขก่อน Merge |
