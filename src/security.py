"""ชั้นความปลอดภัยของแอป — login, sanitize ชื่อไฟล์, rate limit การเทรน

- :func:`require_login`  ด่าน Google login (OIDC ผ่าน st.login) เรียกบนสุดของทุกหน้า
  ถ้ายังไม่ตั้งค่า [auth] ใน secrets จะเข้า "โหมดพัฒนา" (เข้าได้ พร้อมป้ายเตือน)
- :func:`sanitize_filename`  ล้างชื่อไฟล์อัปโหลด กัน path traversal
- :func:`train_cooldown_remaining` / :func:`mark_trained`  เว้นช่วงการเทรนต่อ session
"""

from __future__ import annotations

import os
import re
import time

import streamlit as st

# เว้นช่วงระหว่างการเทรนต่อ session (วินาที) — กันสแปมเทรนถล่ม CPU
TRAIN_COOLDOWN_S = 30


def _auth_configured() -> bool:
    """มีการตั้งค่า [auth] (Google OAuth) ด้วยค่าจริงแล้วหรือยัง

    ค่า placeholder (REPLACE-ME) จากไฟล์โครงถือว่ายังไม่ตั้งค่า →
    เข้าโหมดพัฒนาได้ระหว่างรอ OAuth จริง พอกรอกค่าจริง login เปิดเองทันที
    """
    try:
        auth = st.secrets.get("auth")
        if not auth:
            return False
        client_id = str(auth.get("client_id", ""))
        client_secret = str(auth.get("client_secret", ""))
        if not client_id or not client_secret:
            return False
        if "REPLACE-ME" in client_id or "REPLACE-ME" in client_secret:
            return False
        return True
    except Exception:
        return False


def current_user_email() -> str:
    """คืน email ของผู้ใช้ที่ login อยู่ (หรือ 'dev' ในโหมดพัฒนา)"""
    try:
        if getattr(st.user, "is_logged_in", False):
            return str(st.user.email)
    except Exception:
        pass
    return "dev"


def require_login() -> None:
    """ด่านตรวจ login — เรียกบนสุดของทุกหน้า ถัดจาก inject_style()

    - ตั้งค่า [auth] แล้ว + ยังไม่ login → แสดงหน้า login แล้วหยุด render
    - login แล้ว → แสดงตัวตน + ปุ่มออกจากระบบใน sidebar
    - ยังไม่ตั้งค่า [auth] (รันโลคัล) → โหมดพัฒนา เข้าได้พร้อมป้ายเตือน
    """
    if not _auth_configured():
        st.sidebar.warning("🔓 โหมดพัฒนา — ยังไม่ตั้งค่า Google login (ดู secrets.toml.example)")
        return

    if not st.user.is_logged_in:
        st.markdown("## 🔐 เข้าสู่ระบบ")
        st.markdown("กรุณา login ด้วย Google เพื่อใช้งานระบบคาดการณ์ราคาอสังหาฯ")
        if st.button("เข้าสู่ระบบด้วย Google", type="primary"):
            st.login()
        st.stop()

    with st.sidebar:
        st.caption(f"👤 {st.user.email}")
        if st.button("ออกจากระบบ", use_container_width=True):
            st.logout()


def sanitize_filename(name: str) -> str:
    """ล้างชื่อไฟล์: ตัด path ทิ้ง เหลือเฉพาะอักขระปลอดภัย (กัน path traversal)"""
    base = os.path.basename(name.replace("\\", "/"))
    # \w ไม่ครอบคลุมวรรณยุกต์/สระลอยไทย (combining marks) — อนุญาตบล็อกไทยทั้งช่วงตรงๆ
    safe = re.sub(r"[^\w฀-๿.\- ]", "_", base).strip(". ")
    return safe[:80] or "upload"


def train_cooldown_remaining() -> int:
    """คืนจำนวนวินาทีที่ต้องรอก่อนเทรนครั้งถัดไป (0 = เทรนได้เลย)"""
    last = st.session_state.get("last_train_ts", 0.0)
    remaining = TRAIN_COOLDOWN_S - (time.time() - last)
    return max(0, int(remaining))


def mark_trained() -> None:
    """บันทึกเวลาเทรนล่าสุดของ session นี้ (เริ่มนับ cooldown)"""
    st.session_state["last_train_ts"] = time.time()
