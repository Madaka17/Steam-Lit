"""หน้าสำรวจข้อมูล (EDA)"""

import plotly.express as px
import streamlit as st

from src.data import generate_data
from src.security import require_login
from src.ui import PLOT_SCALE, PLOT_SEQ, inject_style, page_header, style_fig

st.set_page_config(page_title="สำรวจข้อมูล", page_icon="📊", layout="wide")
inject_style()
require_login()


@st.cache_data
def load_data():
    return generate_data()


page_header(
    title="สำรวจข้อมูล",
    kicker="Exploratory Analysis",
    subtitle="รูปแบบการกระจายของราคาและความสัมพันธ์ระหว่างคุณลักษณะของทรัพย์",
)

df = load_data()

st.subheader("การกระจายของราคา")
fig_hist = px.histogram(
    df, x="price", nbins=50, labels={"price": "ราคา (บาท)"},
    color_discrete_sequence=PLOT_SEQ,
)
st.plotly_chart(style_fig(fig_hist), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("พื้นที่ใช้สอย vs ราคา")
    fig_scatter = px.scatter(
        df,
        x="area_sqm",
        y="price",
        color="property_type",
        labels={"area_sqm": "พื้นที่ (ตร.ม.)", "price": "ราคา (บาท)"},
        opacity=0.6,
        color_discrete_sequence=PLOT_SEQ,
    )
    st.plotly_chart(style_fig(fig_scatter), use_container_width=True)

with col2:
    st.subheader("ราคาเฉลี่ยตามทำเล")
    by_district = (
        df.groupby("district")["price"].mean().sort_values(ascending=False)
    )
    fig_bar = px.bar(
        by_district,
        labels={"value": "ราคาเฉลี่ย (บาท)", "district": "ทำเล"},
        color_discrete_sequence=PLOT_SEQ,
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(style_fig(fig_bar), use_container_width=True)

st.subheader("ความสัมพันธ์ระหว่างฟีเจอร์ตัวเลข (Correlation)")
numeric = df.select_dtypes("number")
fig_corr = px.imshow(
    numeric.corr(),
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale=PLOT_SCALE,
    zmin=-1,
    zmax=1,
)
st.plotly_chart(style_fig(fig_corr), use_container_width=True)

st.subheader("สถิติเชิงพรรณนา")
st.dataframe(df.describe(), width="stretch")
