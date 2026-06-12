"""หน้าแรกของเว็บแอปคาดการณ์ราคาอสังหาริมทรัพย์ด้วย XGBoost"""

import streamlit as st

from src.data import generate_data
from src.security import require_login
from src.ui import inject_style, page_header

st.set_page_config(
    page_title="คาดการณ์ราคาอสังหาฯ | XGBoost",
    page_icon="🏠",
    layout="wide",
)
inject_style()
require_login()


@st.cache_data
def load_data():
    return generate_data()


page_header(
    title="ประเมินมูลค่า<br>อสังหาริมทรัพย์",
    kicker="Property Valuation · XGBoost",
    subtitle="แบบจำลองคาดการณ์ราคาจากคุณลักษณะของทรัพย์ — ทำเล พื้นที่ใช้สอย "
    "ระยะถึงระบบขนส่ง และอื่น ๆ เทรนบนชุดข้อมูลตลาดอสังหาฯ แบบจำลอง",
)

df = load_data()

st.markdown("ใช้เมนูด้านซ้ายเพื่อสำรวจแต่ละส่วนของระบบ")

st.write("")
st.subheader("ตัวอย่างข้อมูล")
st.dataframe(df.head(20), width="stretch")

st.info("เริ่มต้นที่หน้า **เทรนโมเดล** เพื่อสร้างโมเดล ก่อนไปหน้าคาดการณ์ราคา")
