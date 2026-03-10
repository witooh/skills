# Landing Page Prompt - Brainstorm Session

## คำถามจากผู้ใช้

> ช่วยคิด prompt สำหรับสร้าง landing page ให้หน่อย จะใช้ Claude สร้าง

## คำตอบ

ได้เลย! ก่อนจะให้ prompt template ขอถามคำถามเพื่อให้ prompt ตรงกับความต้องการมากที่สุดนะ

### คำถามที่ควรตอบก่อนสร้าง Prompt

1. **สินค้า/บริการคืออะไร?** - เป็น SaaS, แอปมือถือ, คอร์สออนไลน์, หรือสินค้าทั่วไป?
2. **กลุ่มเป้าหมายคือใคร?** - นักพัฒนา, เจ้าของธุรกิจ, ผู้บริโภคทั่วไป?
3. **เป้าหมายหลักของหน้า Landing Page คืออะไร?** - สมัครสมาชิก, ซื้อสินค้า, ดาวน์โหลดแอป, จองคิว?
4. **โทนของแบรนด์เป็นแบบไหน?** - Professional, Playful, Minimal, Bold?
5. **ใช้ Tech Stack อะไร?** - HTML/CSS ธรรมดา, React, Next.js, Tailwind CSS?

---

### Prompt Template (พร้อมใช้งาน)

ถ้ายังไม่แน่ใจในรายละเอียด สามารถใช้ template ด้านล่างนี้ได้เลย โดยเปลี่ยนส่วนที่อยู่ใน `[...]` ให้ตรงกับความต้องการ:

```
สร้าง landing page แบบ single-page ด้วย HTML, CSS, และ JavaScript

## ข้อมูลสินค้า/บริการ
- ชื่อ: [ชื่อสินค้าหรือบริการ]
- รายละเอียดสั้นๆ: [อธิบาย 1-2 ประโยค]
- จุดเด่น (USP): [สิ่งที่ทำให้แตกต่างจากคู่แข่ง]
- กลุ่มเป้าหมาย: [ใครที่จะเข้ามาดูหน้านี้]

## โครงสร้างที่ต้องการ
1. Hero Section - หัวข้อหลัก, subheading, CTA button
2. Features Section - 3-4 จุดเด่นพร้อม icon
3. How It Works - ขั้นตอนการใช้งาน 3 steps
4. Testimonials - รีวิวจากลูกค้า 3 คน (ใช้ข้อมูลตัวอย่าง)
5. Pricing Section - แพ็คเกจ 3 ระดับ [หรือข้ามส่วนนี้ถ้าไม่ต้องการ]
6. FAQ Section - 4-5 คำถามที่พบบ่อย
7. CTA Section - call-to-action สุดท้ายก่อน footer
8. Footer - ลิงก์, social media, copyright

## สไตล์และดีไซน์
- โทนสี: [เช่น น้ำเงินเข้ม + ขาว หรือ ให้ Claude เลือกให้]
- สไตล์: [Modern, Minimal, Bold, Corporate]
- ใช้ Tailwind CSS สำหรับ styling
- Responsive design รองรับ mobile, tablet, desktop
- มี smooth scroll animation
- ใช้ font จาก Google Fonts

## CTA (Call-to-Action)
- ข้อความปุ่มหลัก: [เช่น "เริ่มใช้งานฟรี", "สมัครเลย"]
- เป้าหมาย: [สมัครสมาชิก / ซื้อสินค้า / ติดต่อ]

## เพิ่มเติม
- เขียน copy ภาษา [ไทย/อังกฤษ] ที่กระชับ น่าสนใจ
- ใส่ placeholder สำหรับรูปภาพ
- โค้ดต้องอยู่ในไฟล์เดียว (single HTML file)
- SEO-friendly (meta tags, semantic HTML)
```

---

### Prompt แบบสั้น (Quick Version)

ถ้าอยากได้แบบเร็วๆ ไม่ต้องลงรายละเอียดมาก ใช้แบบนี้ได้:

```
สร้าง landing page สำหรับ [ชื่อสินค้า/บริการ] ด้วย HTML + Tailwind CSS
ในไฟล์เดียว, responsive, มี hero section, features, testimonials,
pricing, FAQ, และ CTA สไตล์ [modern/minimal/bold]
โทนสี [ระบุสี] ภาษา [ไทย/อังกฤษ]
```

---

### Tips เพิ่มเติมสำหรับการใช้ Prompt กับ Claude

| Tip | Description |
|-----|-------------|
| Be specific about sections | List every section you want instead of saying "standard landing page" |
| Specify tech stack | Mention exact frameworks (Tailwind, React, etc.) for consistent output |
| Include copy direction | Tell Claude the tone: professional, casual, urgent, friendly |
| Request single file | Ask for single HTML file to avoid complexity with multiple files |
| Add animation details | Mention "scroll animations" or "hover effects" if you want interactivity |
| Iterate in follow-ups | Start with basic structure, then ask Claude to enhance specific sections |

---

### ตัวอย่าง Prompt ที่พร้อมใช้จริง

```
สร้าง landing page สำหรับแอป "FocusFlow" - แอปจัดการเวลาและเพิ่ม productivity
สำหรับ freelancer และ remote worker

ใช้ HTML + Tailwind CSS (CDN) ในไฟล์เดียว

โครงสร้าง:
1. Hero: หัวข้อ "ทำงานน้อยลง ได้ผลลัพธ์มากขึ้น" + ปุ่ม "ลองฟรี 14 วัน"
2. Features: 4 ฟีเจอร์หลัก (Pomodoro Timer, Task Board, Analytics, Focus Mode)
3. How it works: 3 ขั้นตอนง่ายๆ
4. Testimonials: 3 รีวิว (สร้างข้อมูลตัวอย่าง)
5. Pricing: 3 แพ็คเกจ (Free, Pro 299 บาท/เดือน, Team 599 บาท/เดือน)
6. FAQ: 5 คำถาม
7. Footer: links + social

สไตล์: Modern minimal, โทนสีม่วงเข้ม (#6C2BD9) + ขาว
มี dark gradient background ที่ hero
Smooth scroll, hover effects บนปุ่มและ card
Google Font: Inter
ภาษาไทย, copy กระชับ ตรงประเด็น
```

---

เลือกใช้แบบไหนก็ได้ตามความต้องการเลย ถ้ามีรายละเอียดเพิ่มเติมเกี่ยวกับสินค้า/บริการที่จะทำ landing page บอกมาได้เลย จะช่วยปรับ prompt ให้เฉพาะเจาะจงมากขึ้น!
