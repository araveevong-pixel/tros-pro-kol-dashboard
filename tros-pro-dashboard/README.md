# TROS PRO — KOL Campaign Dashboard 2026

แดชบอร์ดเรียลไทม์สำหรับแคมเปญ KOL ของ **TROS Pro Facial BB Powder** — ดีไซน์สไตล์เบนโตะ ขาว-ดำ อัปเดตยอดอัตโนมัติทุก 30 นาทีผ่าน GitHub Actions

แบ่ง 2 แพลตฟอร์ม: **TikTok** (เป้า 10,000,000 วิว · Media 150,000) และ **Facebook** (เป้า 3,500,000 วิว · Media 30,000)

---

## โครงสร้างไฟล์

```
tros-pro-kol-dashboard/
├── index.html                  ← ตัวแดชบอร์ด (เปิดดูได้เลย)
├── brand.json                  ← ตั้งค่าแคมเปญ + KPI
├── scrape_results.json         ← ผลดึงยอดล่าสุด (CI เขียนทับทุกรอบ)
├── scripts/
│   ├── scraper.py              ← ดึงยอด TikTok/Facebook ด้วย yt-dlp
│   ├── update_dashboard.py     ← ฉีดยอดที่ดึงได้เข้า index.html
│   └── update_actual_use.py    ← อัปเดตงบใช้จริงแยกแพลตฟอร์ม
└── .github/workflows/
    └── auto-update.yml         ← cron ทุก 30 นาที
```

---

## Deploy ครั้งแรก (ครั้งเดียวจบ)

ต้องมี `git` และ `gh` (GitHub CLI) ที่ล็อกอินแล้ว (`gh auth login`)

```bash
cd tros-pro-kol-dashboard

git init && git branch -M main
git add . && git commit -m "TROS PRO KOL dashboard"

# สร้าง repo + push  (เปลี่ยน <USER> เป็น GitHub username ของคุณ)
gh repo create <USER>/tros-pro-kol-dashboard --public --source=. --push

# เปิด GitHub Pages
gh api -X POST repos/<USER>/tros-pro-kol-dashboard/pages -f "source[branch]=main" -f "source[path]=/" \
  || gh api -X PUT repos/<USER>/tros-pro-kol-dashboard/pages -f "source[branch]=main" -f "source[path]=/"

# สั่งดึงยอดรอบแรกทันที (ไม่ต้องรอ cron)
gh workflow run auto-update.yml --repo <USER>/tros-pro-kol-dashboard
```

เปิดใช้งานได้ที่: **`https://<USER>.github.io/tros-pro-kol-dashboard/`**
(รอบแรก GitHub Pages ใช้เวลา build ~1–2 นาที)

---

## การอัปเดตยอดอัตโนมัติ

`.github/workflows/auto-update.yml` รันทุก 30 นาที (`*/30 * * * *`):
ติดตั้ง yt-dlp → รัน `scraper.py` → ฉีดผลเข้า `index.html` → commit & push
GitHub Pages redeploy ให้เอง ยอดวิว/ไลก์/คอมเมนต์/แชร์/เซฟ ขยับตามจริง

> ค่า Engagement Rate และ CPV คำนวณสดจากยอดที่ดึงได้ · ค่างบใช้จริง (Actual Use) เก็บในเบราว์เซอร์และคงอยู่ข้ามรอบอัปเดต

---

## เพิ่ม KOL / เพิ่มลิงก์โพสต์ใหม่ (เช่น ฝั่ง Facebook)

**วิธีที่ง่ายที่สุด:** ส่ง Excel `Working` sheet เวอร์ชันล่าสุดให้ลินินสร้างไฟล์ใหม่ให้

**หรือแก้เองในโค้ด:** เปิด `scripts/scraper.py` → เพิ่มเข้า `KOL_LINKS`
```python
"handle_ใหม่": {"url": "https://...", "platform": "Facebook"},
```
แล้วเพิ่มข้อมูลเดียวกันใน `scripts/update_dashboard.py` → `KOL_METADATA` (displayName, platform, followers, budget, profile) จากนั้น commit & push

---

## กรณี yt-dlp ดึงไม่ได้ (เช่น Facebook ที่ต้องล็อกอิน / คลิปจำกัดอายุ)

เปิด `scripts/scraper.py` → ใส่ยอดที่ดูด้วยตาลงใน `MANUAL_OVERRIDE`:
```python
MANUAL_OVERRIDE = {
    "wecanchoose": {"views": 250000, "likes": 3000, "shares": 80, "comments": 40, "saves": 120, "followers": 3000000},
}
```
commit & push แล้วรอบถัดไปจะใช้ค่านี้แทน

---

## หมายเหตุ Facebook

ตอนนี้มีลิงก์ TikTok ที่โพสต์แล้ว 17 โพสต์ · ฝั่ง Facebook (เพจผู้บริโภค `wecanchoose`) ยังรอโพสต์
เมื่อลิงก์ Facebook มาแล้ว เพิ่มตามหัวข้อด้านบน — `scraper.py` รองรับทั้ง 2 แพลตฟอร์มในตัวเดียว

---

*สร้างด้วย Claude Cowork · kol-dashboard-generator · 23 ก.ค. 2026*
