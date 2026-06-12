"""หน้าเทรนโมเดล — โหมดเกม: ปรับ "พลัง" ของโมเดลแล้วทำคะแนนความแม่นยำ"""

import os
import time

import plotly.express as px
import streamlit as st

from src.data import generate_data
from src.model import save_model, train_model
from src.security import (
    current_user_email,
    mark_trained,
    require_login,
    train_cooldown_remaining,
)
from src.storage import (
    ValidationError,
    read_upload,
    save_upload,
    validate_dataset,
)
from src.ui import (
    PLOT_SEQ,
    grade_for,
    inject_style,
    page_header,
    score_card,
    style_fig,
)

st.set_page_config(page_title="เทรนโมเดล", page_icon="🎮", layout="wide")
inject_style()
require_login()


@st.cache_data
def load_data():
    return generate_data()


page_header(
    title="โหมดฝึกโมเดล",
    kicker="Training Challenge",
    subtitle="ปรับ ‘พลัง’ ของโมเดล แล้วเทรนให้ทำคะแนนความแม่นยำ (R²) ให้สูงที่สุด",
)

df = load_data()
best = st.session_state.get("best_score", 0.0)

# ----- เลือกแหล่งข้อมูลเทรน -----
st.markdown("##### 📂 แหล่งข้อมูลเทรน")
source = st.radio(
    "เลือกชุดข้อมูล",
    ["ข้อมูลจำลอง (ในระบบ)", "อัปโหลดไฟล์ของฉัน"],
    horizontal=True,
    label_visibility="collapsed",
)
if source == "ข้อมูลจำลอง (ในระบบ)":
    st.caption("👉 เลือก **อัปโหลดไฟล์ของฉัน** ด้านบน เพื่อใช้ข้อมูล CSV/Excel ของคุณเอง")

train_df = df
data_source = "synthetic"
upload = None  # เก็บไฟล์ที่อัปโหลดไว้บันทึกตอนกดเทรน
ready = True

if source == "อัปโหลดไฟล์ของฉัน":
    ready = False
    upload = st.file_uploader(
        "อัปโหลด CSV หรือ Excel — ต้องมีคอลัมน์ตาม schema "
        "(area_sqm, bedrooms, bathrooms, age_years, floor, distance_bts_km, "
        "property_type, district, price)",
        type=["csv", "xlsx", "xls"],
    )
    if upload is not None:
        try:
            valid = validate_dataset(read_upload(upload.name, upload.getvalue()))
        except ValidationError as exc:
            st.error(f"❌ {exc}")
        else:
            train_df = valid
            data_source = "uploaded"
            ready = True
            st.success(f"✅ ไฟล์ผ่านการตรวจ {len(valid):,} แถว — พร้อมเทรน")
            st.dataframe(valid.head(10), width="stretch")
    else:
        st.info("อัปโหลดไฟล์เพื่อเทรนด้วยข้อมูลของคุณเอง")

st.write("")

# ----- ตัวควบคุมแบบเกม -----
st.markdown("##### ⚙️ ปรับพลังโมเดล")
c1, c2, c3 = st.columns(3)
with c1:
    n_estimators = st.slider("🌳 จำนวนต้นไม้", 100, 800, 400, 50)
with c2:
    max_depth = st.slider("🪜 ความลึก", 2, 10, 5, 1)
with c3:
    learning_rate = st.select_slider(
        "⚡ อัตราการเรียนรู้", options=[0.01, 0.03, 0.05, 0.1, 0.2], value=0.05
    )

st.write("")
cooldown = train_cooldown_remaining()
if cooldown:
    st.warning(f"⏳ เพิ่งเทรนไปหมาดๆ — รออีก {cooldown} วินาทีก่อนเทรนรอบถัดไป")
go = st.button(
    "▶  เริ่มเทรน",
    type="primary",
    use_container_width=True,
    disabled=(not ready) or cooldown > 0,
)

if go:
    progress = st.progress(0, text="กำลังเตรียมข้อมูล...")
    for pct, msg in [
        (15, "แบ่งชุดข้อมูลฝึก/ทดสอบ..."),
        (45, "กำลังปลูกต้นไม้ตัดสินใจ..."),
        (78, "กำลังเรียนรู้รูปแบบราคา..."),
        (95, "ประเมินผลความแม่นยำ..."),
    ]:
        time.sleep(0.28)
        progress.progress(pct, text=msg)

    result = train_model(
        train_df,
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
    )
    save_model(result.pipeline)
    st.session_state["train_result"] = result
    st.session_state["model_source"] = data_source
    mark_trained()

    # บันทึกสำรองไฟล์อัปโหลดลง Upload Archive เฉพาะตอนเทรนจริง
    if data_source == "uploaded" and upload is not None:
        backup_path = save_upload(
            upload.name, upload.getvalue(), user=current_user_email()
        )
        st.toast(f"💾 สำรองไฟล์ไว้ที่ {os.path.relpath(backup_path)}")

    progress.progress(100, text="เสร็จสิ้น! 🎉")
    time.sleep(0.25)
    progress.empty()

    score = grade_for(result.r2)[0]
    if score > best:
        st.session_state["best_score"] = score
        best = score
    if score >= 90:
        st.balloons()

# ----- ผลลัพธ์ -----
result = st.session_state.get("train_result")

if result is None:
    st.info("ปรับค่าพลังด้านบน แล้วกด ▶ เริ่มเทรน เพื่อเริ่มทำคะแนน")
else:
    score, grade, color, msg = grade_for(result.r2)
    score_card(score, grade, color, msg, best)

    st.write("")
    m1, m2, m3 = st.columns(3)
    m1.metric("R²", f"{result.r2:.3f}")
    m2.metric("RMSE", f"{result.rmse:,.0f} ฿")
    m3.metric("MAE", f"{result.mae:,.0f} ฿")

    with st.expander("🔍 ดูรายละเอียดเชิงเทคนิค (กราฟ)"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("ค่าจริง vs ค่าทำนาย")
            fig = px.scatter(
                x=result.y_test,
                y=result.y_pred,
                labels={"x": "ราคาจริง (บาท)", "y": "ราคาทำนาย (บาท)"},
                opacity=0.5,
                color_discrete_sequence=PLOT_SEQ,
            )
            lo = min(result.y_test.min(), result.y_pred.min())
            hi = max(result.y_test.max(), result.y_pred.max())
            fig.add_shape(
                type="line", x0=lo, y0=lo, x1=hi, y1=hi,
                line=dict(dash="dash", color="#8C3820"),
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)

        with col2:
            st.subheader("ความสำคัญของฟีเจอร์")
            imp = result.feature_importance.head(12).sort_values()
            fig_imp = px.bar(
                imp, orientation="h",
                labels={"value": "importance", "index": "ฟีเจอร์"},
                color_discrete_sequence=PLOT_SEQ,
            )
            fig_imp.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig_imp), use_container_width=True)
