# 🏠 ระบบคาดการณ์ราคาอสังหาริมทรัพย์ (XGBoost)

เว็บแอป Streamlit สาธิตการคาดการณ์ราคาอสังหาริมทรัพย์ด้วยโมเดล **XGBoost**
บนชุดข้อมูลจำลองแบบไทย (คอนโด/บ้านเดี่ยว/ทาวน์เฮาส์) หรือข้อมูลที่ผู้ใช้อัปโหลดเอง

## ฟีเจอร์

- **📊 สำรวจข้อมูล (EDA)** — การกระจายราคา, พื้นที่ vs ราคา, ราคาเฉลี่ยตามทำเล, correlation
- **🎮 เทรนโมเดล** — เทรน XGBoost ปรับ hyperparameter ได้, ดู RMSE/MAE/R², กราฟค่าจริง-vs-ทำนาย, feature importance
- **📤 อัปโหลดข้อมูลเอง** — เทรนจากไฟล์ CSV/Excel ของคุณ (ต้องมีคอลัมน์ตาม Canonical Schema ดู `CONTEXT.md`)
  ไฟล์ที่ผ่านการตรวจถูกสำรองลง `data/uploads/` พร้อม audit log
- **💰 คาดการณ์ราคา** — กรอกข้อมูลทรัพย์แล้วประเมินราคา (เทรนอัตโนมัติถ้ายังไม่มีโมเดล)
- **🎨 สลับธีม** — Toggle มุมบนซ้าย: 🌙 Dark / ☀️ Day Dream (มิ้นต์สว่าง)

## ความปลอดภัย (สำหรับเปิด public)

- **Google login (OIDC)** ผ่าน `st.login` — บังคับทุกหน้าเมื่อตั้งค่า `[auth]` แล้ว
  (รันโลคัลโดยไม่ตั้งค่า = โหมดพัฒนา เข้าได้พร้อมป้ายเตือน)
- จำกัดไฟล์อัปโหลด 10MB + เพดาน 100,000 แถว (กัน Excel bomb)
- Sanitize ชื่อไฟล์ (กัน path traversal), โควตา `data/uploads/` รวม 200MB (เต็มแล้วลบเก่าสุด)
- Rate limit การเทรน 30 วินาที/ครั้ง/session + audit log ผู้อัปโหลด

ตั้งค่า Google OAuth: คัดลอก `.streamlit/secrets.toml.example` เป็น
`.streamlit/secrets.toml` แล้วกรอกค่าจริง (ขั้นตอนอยู่ในไฟล์ — ห้าม commit)

## การติดตั้ง

> **macOS:** XGBoost ต้องการ OpenMP runtime ติดตั้งก่อนด้วย
> ```bash
> brew install libomp
> ```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## รันแอป

```bash
streamlit run app.py
```

แล้วเปิดเบราว์เซอร์ที่ http://localhost:8501

## รันเทสต์

```bash
pip install pytest
pytest
```

## Deploy (Streamlit Community Cloud)

1. Push repo ขึ้น GitHub
2. สร้างแอปที่ https://share.streamlit.io ชี้ไปที่ `app.py`
3. วางเนื้อหา `[auth]` (จาก secrets.toml.example ที่กรอกค่าจริงแล้ว) ใน App settings → Secrets
   โดยใช้ redirect URI ของโดเมนแอป: `https://<your-app>.streamlit.app/oauth2callback`

> ⚠️ ไฟล์ใน `data/uploads/` และ `model.joblib` บน Community Cloud
> หายเมื่อแอป restart (filesystem ชั่วคราว)

## โครงสร้างโปรเจกต์

```
real-estate-predictor/
├── app.py                  # หน้าแรก
├── pages/                  # หน้าย่อย (EDA, เทรน, คาดการณ์)
├── src/
│   ├── data.py             # สร้างข้อมูลจำลอง + Canonical Schema
│   ├── model.py            # train / predict / save / load
│   ├── storage.py          # อ่าน/ตรวจ/สำรองไฟล์อัปโหลด
│   ├── security.py         # login, sanitize, rate limit
│   └── ui.py               # ระบบดีไซน์ + ธีม Dark/Day Dream
├── tests/                  # pytest (model, storage, security)
├── docs/adr/               # บันทึกการตัดสินใจเชิงสถาปัตยกรรม
├── CONTEXT.md              # อภิธานศัพท์ของโปรเจกต์
└── requirements.txt
```
