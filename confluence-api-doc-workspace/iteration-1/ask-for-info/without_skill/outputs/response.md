# การซิงค์ API Doc ไป Confluence

เพื่อช่วยได้อย่างถูกต้อง ต้องการข้อมูลเพิ่มเติมก่อนครับ:

## ข้อมูลที่ต้องการ

**เกี่ยวกับ API Doc:**
- API Doc อยู่ในรูปแบบอะไร? (OpenAPI/Swagger, Postman Collection, Markdown, อื่นๆ)
- ไฟล์อยู่ที่ไหน? (local file, URL, Git repository)

**เกี่ยวกับ Confluence:**
- Confluence URL คืออะไร?
- จะ sync ไปยัง Space และ Page ไหน?
- มี API Token หรือ credentials สำหรับ Confluence แล้วหรือยัง?

**เกี่ยวกับความต้องการ:**
- ต้องการ sync แบบ manual หรือ automated (เช่น CI/CD)?
- ต้องการ sync ครั้งเดียว หรือต้องการให้ sync อัตโนมัติเมื่อมีการอัปเดต?

## วิธีที่นิยมใช้

1. **confluence-swagger-ui** - สำหรับ Swagger/OpenAPI
2. **Atlassian CLI** - ใช้ command line sync content
3. **Python script + Confluence REST API** - เขียน script เอง
4. **GitHub Actions / CI/CD** - sync อัตโนมัติเมื่อ merge

ช่วยบอกรายละเอียดเพิ่มเติมได้เลยครับ จะได้แนะนำวิธีที่เหมาะสมที่สุด
