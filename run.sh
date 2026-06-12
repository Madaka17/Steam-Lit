#!/usr/bin/env bash
# เปิดเซิร์ฟเวอร์ Streamlit แล้วเด้งเบราว์เซอร์อัตโนมัติ
set -e
cd "$(dirname "$0")"

# สร้าง venv + ติดตั้ง dependencies อัตโนมัติถ้ายังไม่มี
if [ ! -d ".venv" ]; then
  echo "🔧 สร้าง virtualenv และติดตั้ง dependencies ครั้งแรก..."
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip -q
  .venv/bin/pip install -r requirements.txt -q
fi

URL="http://localhost:8501"
# เปิดเบราว์เซอร์หลังเซิร์ฟเวอร์พร้อม (รอ health check)
(
  for _ in $(seq 1 30); do
    if curl -s -o /dev/null "$URL/_stcore/health"; then
      open "$URL"; break
    fi
    sleep 1
  done
) &

echo "🚀 เปิดแอปที่ $URL  (กด Ctrl+C เพื่อหยุด)"
exec .venv/bin/streamlit run app.py --server.port 8501 --server.headless true
