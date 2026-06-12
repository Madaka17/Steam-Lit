"""หน้าคาดการณ์ราคา — กรอกข้อมูลทรัพย์แล้วให้โมเดลประเมินราคา"""

import streamlit as st

from src.data import DISTRICTS, PROPERTY_TYPES, generate_data
from src.model import (
    load_model,
    model_exists,
    predict_price,
    save_model,
    train_model,
)
from src.security import require_login
from src.ui import inject_style, page_header

st.set_page_config(page_title="คาดการณ์ราคา", page_icon="💰", layout="wide")
inject_style()
require_login()


@st.cache_data
def load_data():
    return generate_data()


def get_pipeline():
    """คืน pipeline ที่พร้อมใช้ — จาก session, ไฟล์, หรือเทรนใหม่อัตโนมัติ"""
    if "train_result" in st.session_state:
        return st.session_state["train_result"].pipeline
    if model_exists():
        return load_model()
    with st.spinner("ยังไม่มีโมเดล — กำลังเทรนอัตโนมัติ..."):
        result = train_model(load_data())
        save_model(result.pipeline)
        st.session_state["train_result"] = result
    return result.pipeline


page_header(
    title="คาดการณ์ราคา",
    kicker="Instant Valuation",
    subtitle="กรอกคุณลักษณะของทรัพย์ แล้วให้แบบจำลองประเมินมูลค่าทันที",
)

pipeline = get_pipeline()

_SOURCE_LABEL = {"synthetic": "ข้อมูลจำลอง (ในระบบ)", "uploaded": "ไฟล์ที่อัปโหลด"}
_active_source = _SOURCE_LABEL.get(st.session_state.get("model_source"))
if _active_source:
    st.caption(f"🧠 โมเดลปัจจุบันเทรนจาก: **{_active_source}**")

with st.form("predict_form"):
    c1, c2 = st.columns(2)
    with c1:
        property_type = st.selectbox("ประเภท", list(PROPERTY_TYPES))
        district = st.selectbox("ทำเล", list(DISTRICTS))
        area_sqm = st.number_input(
            "พื้นที่ใช้สอย (ตร.ม.)", min_value=20.0, max_value=400.0, value=60.0, step=1.0
        )
        distance_bts_km = st.number_input(
            "ระยะถึง BTS/MRT (กม.)", min_value=0.1, max_value=20.0, value=1.5, step=0.1
        )
    with c2:
        bedrooms = st.slider("ห้องนอน", 1, 5, 2)
        bathrooms = st.slider("ห้องน้ำ", 1, 4, 1)
        age_years = st.slider("อายุอาคาร (ปี)", 0, 30, 5)
        floor = st.slider("ชั้น", 1, 40, 8)

    submitted = st.form_submit_button("ประเมินราคา", type="primary")

if submitted:
    features = {
        "area_sqm": area_sqm,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age_years,
        "floor": floor,
        "distance_bts_km": distance_bts_km,
        "property_type": property_type,
        "district": district,
    }
    price = predict_price(pipeline, features)
    st.markdown(
        f"""
        <div class="price-result">
          <div>
            <span class="pr-label">ราคาประเมิน</span>
            <span class="pr-value">{price:,.0f}<small>บาท</small></span>
          </div>
          <div class="pr-unit">
            ราคาต่อตารางเมตร<br><b>{price / area_sqm:,.0f}</b> บาท/ตร.ม.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
