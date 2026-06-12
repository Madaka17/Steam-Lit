"""ระบบดีไซน์กลางของแอป — ธีม Dark Futuristic / AI-Tech

นีออนฟ้า-เขียว, aurora เรืองแสง, การ์ดกระจกเรืองแสง, ตัวอักษรไล่เฉด,
โลโก้ AI มุมขวาบน — ใช้ helper ร่วมกันทุกหน้า
"""

import streamlit as st

# ===== ชุดตัวแปรสีของแต่ละธีม (เปลี่ยนชุดเดียว ทั้งแอปเปลี่ยนตาม) =====
_DARK_VARS = """
  --bg:#070B14;
  --bg-2:#0C1322;
  --panel:rgba(18,28,46,.55);
  --panel-2:rgba(22,34,56,.7);
  --cyan:#22E3D0;
  --cyan-2:#5EEAD4;
  --blue:#38BDF8;
  --green:#4ADE80;
  --ink:#DCE7F4;
  --ink-soft:#8195B2;
  --line:rgba(120,165,210,.16);
  --glow:rgba(34,227,208,.55);
  --grad-hi:#EAF2FB;
  --btn-ink:#04140F;
  --result-grad:linear-gradient(135deg, rgba(13,22,38,.95), rgba(8,13,22,.95));
  --score-grad:linear-gradient(160deg, rgba(13,22,38,.95), rgba(8,13,22,.98));
  --sidebar-bg:rgba(8,13,22,.85);
"""

# Day Dream — Mint Cloud: พื้นมิ้นต์อ่อน แอคเซนต์มิ้นต์-ฟ้า ตัวอักษรเขียวเข้ม
_DAYDREAM_VARS = """
  --bg:#ECFDF7;
  --bg-2:#D6F7EC;
  --panel:rgba(255,255,255,.72);
  --panel-2:rgba(255,255,255,.9);
  --cyan:#14B8A6;
  --cyan-2:#0E9488;
  --blue:#0EA5E9;
  --green:#16A34A;
  --ink:#14403A;
  --ink-soft:#5B7C74;
  --line:rgba(20,184,166,.22);
  --glow:rgba(20,184,166,.40);
  --grad-hi:#0B3B33;
  --btn-ink:#FFFFFF;
  --result-grad:linear-gradient(135deg, #FFFFFF, #E6FBF3);
  --score-grad:linear-gradient(160deg, #FFFFFF, #E6FBF3);
  --sidebar-bg:rgba(255,255,255,.82);
"""

_THEMES = {"Dark": _DARK_VARS, "Day Dream": _DAYDREAM_VARS}

# grain texture บางๆ
_GRAIN = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' "
    "numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E"
    "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"
)

# ribbon aurora — เส้นแสงโค้งไหลเรืองแสง (เลเยอร์พื้นหลัง)
_AURORA = """
<div class="aurora">
  <svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="ag1" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stop-color="#22E3D0" stop-opacity="0"/>
        <stop offset="45%" stop-color="#22E3D0" stop-opacity="1"/>
        <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="ag2" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stop-color="#4ADE80" stop-opacity="0"/>
        <stop offset="50%" stop-color="#5EEAD4" stop-opacity="1"/>
        <stop offset="100%" stop-color="#22E3D0" stop-opacity="0"/>
      </linearGradient>
      <filter id="agblur" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3"/>
      </filter>
    </defs>
    <g fill="none" stroke-linecap="round" filter="url(#agblur)">
      <path class="rb" style="animation-delay:0s"   d="M-60 880 C 260 700 380 770 620 560 S 940 520 1240 300" stroke="url(#ag1)" stroke-width="3"/>
      <path class="rb" style="animation-delay:-4s"  d="M-50 820 C 210 770 440 690 580 610 S 860 600 1160 410" stroke="url(#ag2)" stroke-width="2.4"/>
      <path class="rb" style="animation-delay:-8s"  d="M-40 910 C 320 820 520 850 780 700 S 1140 660 1480 470" stroke="url(#ag1)" stroke-width="2"/>
      <path class="rb" style="animation-delay:-2s"  d="M1500 50  C 1260 140 1160 80 990 230 S 770 250 600 390"  stroke="url(#ag2)" stroke-width="2.6"/>
      <path class="rb" style="animation-delay:-6s"  d="M1505 150 C 1300 190 1180 180 1040 300 S 880 360 760 470" stroke="url(#ag1)" stroke-width="2"/>
    </g>
  </svg>
</div>
"""

# โลโก้ AI (neural network) มุมขวาบน
_EMBLEM = """
<div class="brand">
  <svg viewBox="0 0 100 100" width="46" height="46" class="brand-svg">
    <g stroke="#22E3D0" stroke-width="1.6" fill="none" opacity=".85">
      <path d="M50 24 L27 48 M50 24 L73 48 M27 52 L41 76 M73 52 L59 76 M30 50 L70 50 M44 78 L56 78"/>
      <circle cx="50" cy="20"/><circle cx="50" cy="20" r="6"/>
      <circle cx="24" cy="50" r="6"/><circle cx="76" cy="50" r="6"/>
      <circle cx="41" cy="80" r="6"/><circle cx="59" cy="80" r="6"/>
    </g>
    <g fill="#5EEAD4">
      <circle cx="50" cy="20" r="2.4"/><circle cx="24" cy="50" r="2.4"/>
      <circle cx="76" cy="50" r="2.4"/><circle cx="41" cy="80" r="2.4"/>
      <circle cx="59" cy="80" r="2.4"/>
    </g>
  </svg>
  <div class="brand-text">VALUATION · XGBOOST<br><span>ANALYTICS</span></div>
</div>
<div class="spark"></div>
"""

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@500;600;700&family=IBM+Plex+Sans+Thai:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
__ROOT__
}

/* ---------- base ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"]{
  background-color: var(--bg);
  color: var(--ink);
  font-family:'IBM Plex Sans Thai', sans-serif;
}
/* aurora glow + grain */
[data-testid="stAppViewContainer"]::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(55% 45% at 88% 8%, rgba(34,227,208,.16), transparent 60%),
    radial-gradient(50% 55% at 6% 92%, rgba(56,189,248,.15), transparent 60%),
    radial-gradient(45% 40% at 60% 105%, rgba(74,222,128,.10), transparent 60%);
  animation:drift 16s ease-in-out infinite;
}
[data-testid="stAppViewContainer"]::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  opacity:.05; background-image:url("__GRAIN__"); background-size:160px;
}
@keyframes drift{ 0%,100%{transform:translate(0,0);} 50%{transform:translate(-12px,14px);} }

/* ribbon aurora — เส้นแสงไหล */
.aurora{ position:fixed; inset:0; z-index:0; pointer-events:none; opacity:1; }
.aurora svg{ width:100%; height:100%; display:block; }
.aurora .rb{
  stroke-dasharray:1000 480; stroke-dashoffset:0;
  animation:flow 18s linear infinite, glowpulse 7s ease-in-out infinite;
}
@keyframes flow{ to{ stroke-dashoffset:-1480; } }
@keyframes glowpulse{ 0%,100%{opacity:.75;} 50%{opacity:1;} }

[data-testid="stHeader"]{ background:transparent; }
[data-testid="stMainBlockContainer"], .block-container{
  position:relative; z-index:1; max-width:1080px; padding-top:2.4rem;
}

/* ---------- brand emblem + sparkle ---------- */
.brand{
  position:fixed; top:74px; right:42px; z-index:0; pointer-events:none;
  display:flex; align-items:center; gap:.7rem; opacity:.9;
  animation:fadein 1.2s ease both .3s;
}
.brand-svg{ filter:drop-shadow(0 0 8px var(--glow)); }
.brand-text{
  font-family:'IBM Plex Mono', monospace; font-size:.62rem; letter-spacing:.18em;
  color:var(--cyan-2); line-height:1.5; text-align:left;
}
.brand-text span{ color:var(--ink-soft); }
.spark{
  position:fixed; bottom:46px; right:60px; width:26px; height:26px; z-index:0; pointer-events:none;
  background:
    radial-gradient(circle, var(--cyan) 0 1px, transparent 2px),
    conic-gradient(from 0deg, transparent, var(--cyan-2), transparent 30%);
  -webkit-mask:radial-gradient(circle at center, #000 60%, transparent 62%);
  filter:drop-shadow(0 0 6px var(--glow)); opacity:.6; animation:twinkle 4s ease-in-out infinite;
}
.spark::before{
  content:"✦"; position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  color:var(--cyan-2); font-size:22px; filter:drop-shadow(0 0 8px var(--glow));
}
@keyframes twinkle{ 0%,100%{opacity:.35; transform:scale(.85);} 50%{opacity:.9; transform:scale(1.1);} }
@keyframes fadein{ from{opacity:0;} to{opacity:.9;} }

/* ---------- typography ---------- */
h1,h2,h3,h4{ font-family:'Kanit', sans-serif; color:var(--ink); font-weight:600; letter-spacing:.01em; }
h1{ font-size:2.9rem; line-height:1.08; }
h2{ font-size:1.7rem; }
h3{ font-size:1.2rem; color:var(--cyan-2); }
p, li, .stMarkdown, label, span{ color:var(--ink); }

/* ---------- editorial header ---------- */
.eh{ animation:rise .7s cubic-bezier(.2,.7,.2,1) both; margin-bottom:1.7rem; }
.eh .kicker{
  font-family:'IBM Plex Mono', monospace; font-size:.72rem; font-weight:500;
  letter-spacing:.26em; text-transform:uppercase; color:var(--cyan);
  display:flex; align-items:center; gap:.7rem; margin-bottom:.8rem;
  text-shadow:0 0 10px rgba(34,227,208,.4);
}
.eh .kicker::before{
  content:""; width:34px; height:2px; background:var(--cyan); display:inline-block;
  box-shadow:0 0 8px var(--glow); animation:grow .8s ease both .15s;
}
@keyframes grow{ from{width:0; opacity:0;} to{width:34px; opacity:1;} }
.eh h1.eh-title{
  font-family:'Kanit', sans-serif; font-size:3.3rem; line-height:1.05; margin:0; font-weight:700;
  background:linear-gradient(100deg, var(--grad-hi) 0%, var(--cyan-2) 45%, var(--blue) 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  filter:drop-shadow(0 2px 18px rgba(34,227,208,.25));
}
.eh .eh-sub{ font-size:1rem; color:var(--ink-soft); max-width:46rem; margin-top:.9rem; line-height:1.6; font-weight:300; }
.eh .rule{ height:1px; margin-top:1.4rem; background:linear-gradient(90deg, var(--cyan), transparent 70%); opacity:.5; }
@keyframes rise{ from{opacity:0; transform:translateY(14px);} to{opacity:1; transform:none;} }

/* ---------- glow metric cards ---------- */
.gcard{
  position:relative; background:var(--panel); border:1px solid var(--line);
  border-radius:14px; padding:1.3rem 1.4rem 1.2rem; overflow:hidden;
  backdrop-filter:blur(8px); transition:transform .25s ease, box-shadow .25s ease, border-color .25s;
  animation:rise .6s ease both;
}
.gcard::before{
  content:""; position:absolute; inset:0; border-radius:14px; padding:1px; pointer-events:none;
  background:linear-gradient(135deg, rgba(34,227,208,.6), transparent 40%, rgba(56,189,248,.4));
  -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite:xor; mask-composite:exclude; opacity:.8;
}
.gcard:hover{ transform:translateY(-6px); border-color:rgba(34,227,208,.5); box-shadow:0 14px 40px rgba(34,227,208,.18); }
.gcard-top{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:1rem; }
.gcard-ico{
  width:44px; height:44px; border-radius:11px; display:flex; align-items:center; justify-content:center;
  background:rgba(34,227,208,.10); border:1px solid rgba(34,227,208,.3); color:var(--cyan-2);
  box-shadow:0 0 18px rgba(34,227,208,.15) inset;
}
.gcard-ico svg{ width:22px; height:22px; }
.gcard-spark{ opacity:.85; }
.gcard-label{
  font-family:'IBM Plex Mono', monospace; font-size:.68rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-soft);
}
.gcard-value{
  font-family:'Kanit', sans-serif; font-size:1.75rem; font-weight:600; margin-top:.2rem;
  background:linear-gradient(100deg, var(--grad-hi), var(--cyan-2));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}

/* ---------- native st.metric (fallback) ---------- */
[data-testid="stMetric"]{
  background:var(--panel); border:1px solid var(--line); border-radius:12px;
  padding:1rem 1.2rem; backdrop-filter:blur(8px);
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s;
}
[data-testid="stMetric"]:hover{ transform:translateY(-5px); border-color:rgba(34,227,208,.5); box-shadow:0 12px 30px rgba(34,227,208,.16); }
[data-testid="stMetricLabel"] p{
  font-family:'IBM Plex Mono', monospace; text-transform:uppercase; letter-spacing:.14em;
  font-size:.66rem; color:var(--ink-soft);
}
[data-testid="stMetricValue"]{ font-family:'Kanit', sans-serif; font-size:1.7rem; color:var(--cyan-2); }

/* ---------- buttons ---------- */
.stButton>button, .stFormSubmitButton>button, [data-testid="stBaseButton-primary"]{
  background:linear-gradient(120deg, rgba(34,227,208,.18), rgba(56,189,248,.18));
  color:var(--cyan-2); border:1px solid rgba(34,227,208,.5); border-radius:9px;
  font-family:'Kanit', sans-serif; font-weight:600; letter-spacing:.05em;
  padding:.55rem 1.6rem; transition:all .2s ease; position:relative; overflow:hidden;
  box-shadow:0 0 0 rgba(34,227,208,0);
}
.stButton>button::after, .stFormSubmitButton>button::after{
  content:""; position:absolute; top:0; left:-130%; width:55%; height:100%;
  background:linear-gradient(120deg, transparent, rgba(94,234,212,.45), transparent);
  transform:skewX(-20deg); transition:left .6s ease;
}
.stButton>button:hover::after, .stFormSubmitButton>button:hover::after{ left:150%; }
.stButton>button:hover, .stFormSubmitButton>button:hover{
  border-color:var(--cyan); color:var(--btn-ink);
  background:linear-gradient(120deg, var(--cyan), var(--blue));
  transform:translateY(-2px); box-shadow:0 8px 26px rgba(34,227,208,.4);
}

/* ---------- inputs / widgets ---------- */
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label{ color:var(--ink-soft); font-size:.85rem; font-weight:500; }
[data-baseweb="select"]>div, [data-testid="stNumberInputContainer"]{
  background:var(--panel-2); border-radius:8px; border-color:var(--line); color:var(--ink);
}
[data-testid="stSlider"] [role="slider"]{ background:var(--cyan) !important; box-shadow:0 0 10px var(--glow) !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"]{ background:var(--cyan) !important; }
[data-testid="stForm"]{
  background:var(--panel); border:1px solid var(--line); border-radius:14px;
  padding:1.6rem 1.8rem; backdrop-filter:blur(8px);
}
[data-testid="stExpander"]{ border:1px solid var(--line); border-radius:12px; background:var(--panel); backdrop-filter:blur(6px); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{ background:var(--sidebar-bg); border-right:1px solid var(--line); backdrop-filter:blur(10px); }
[data-testid="stSidebarNav"] a span{ font-family:'IBM Plex Sans Thai'; font-size:.92rem; color:var(--ink-soft); }
[data-testid="stSidebarNav"] a:hover span{ color:var(--ink); }
[data-testid="stSidebarNav"] a[aria-current="page"]{ background:rgba(34,227,208,.12); border-radius:8px; box-shadow:inset 0 0 0 1px rgba(34,227,208,.3); }
[data-testid="stSidebarNav"] a[aria-current="page"] span{ color:var(--cyan-2); font-weight:600; }

/* ---------- dataframe / alerts ---------- */
[data-testid="stDataFrame"]{ border:1px solid var(--line); border-radius:12px; overflow:hidden; }
[data-testid="stAlert"]{ border-radius:10px; border:1px solid rgba(34,227,208,.3); background:var(--panel); color:var(--ink); }
[data-testid="stAlertContainer"]{ border-left:3px solid var(--cyan); }

/* ---------- price result ---------- */
.price-result{
  background:var(--result-grad);
  border:1px solid rgba(34,227,208,.35); color:var(--ink); border-radius:14px;
  padding:1.8rem 2rem; margin-top:.4rem; display:flex; align-items:baseline;
  justify-content:space-between; flex-wrap:wrap; gap:1rem; position:relative; overflow:hidden;
  animation:rise .5s ease both; box-shadow:0 0 40px rgba(34,227,208,.12);
}
.price-result::after{ content:""; position:absolute; top:0; left:0; width:4px; height:100%; background:var(--cyan); box-shadow:0 0 18px var(--glow); }
.price-result .pr-label{
  font-family:'IBM Plex Mono', monospace; font-size:.7rem; letter-spacing:.22em; text-transform:uppercase;
  color:var(--cyan); display:block; margin-bottom:.5rem;
}
.price-result .pr-value{
  font-family:'Kanit', sans-serif; font-size:2.9rem; font-weight:700; line-height:1;
  background:linear-gradient(100deg, #EAF2FB, var(--cyan-2));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.price-result .pr-value small{ font-size:1.1rem; font-weight:400; color:var(--ink-soft); margin-left:.4rem; -webkit-text-fill-color:var(--ink-soft); }
.price-result .pr-unit{ font-family:'IBM Plex Mono', monospace; font-size:.85rem; color:var(--ink-soft); text-align:right; line-height:1.6; }
.price-result .pr-unit b{ color:var(--green); font-family:'Kanit', sans-serif; font-size:1.3rem; }

/* ---------- training game ---------- */
.score-card{
  text-align:center; border-radius:16px; padding:2.2rem 2rem 1.8rem; position:relative; overflow:hidden;
  background:var(--score-grad);
  border:1px solid rgba(34,227,208,.35); color:var(--ink);
  box-shadow:0 18px 50px rgba(0,0,0,.45), 0 0 60px rgba(34,227,208,.10);
  animation:pop .55s cubic-bezier(.2,1.35,.4,1) both;
}
.score-card::before{
  content:""; position:absolute; inset:0; pointer-events:none; opacity:.6;
  background:radial-gradient(120% 130% at 50% -25%, rgba(34,227,208,.35), transparent 60%);
}
.score-card .sc-label{ position:relative; font-family:'IBM Plex Mono', monospace; font-size:.72rem; letter-spacing:.3em; text-transform:uppercase; color:var(--cyan); }
.score-card .grade{
  position:relative; font-family:'Kanit', sans-serif; font-weight:700; font-size:5.6rem; line-height:1;
  margin:.3rem 0 .2rem; animation:gradePop .7s cubic-bezier(.2,1.6,.4,1) both .12s;
}
.score-card .score-num{ position:relative; font-family:'Kanit', sans-serif; font-size:1.7rem; color:var(--ink); }
.score-card .score-num span{ font-size:.95rem; color:var(--ink-soft); margin-left:.2rem; }
.score-card .sc-msg{ position:relative; margin-top:.5rem; color:var(--ink-soft); font-size:1rem; }
.score-card .sc-best{
  position:relative; margin-top:1rem; display:inline-block; font-family:'IBM Plex Mono', monospace;
  font-size:.78rem; color:var(--cyan-2); border:1px solid rgba(34,227,208,.4);
  border-radius:999px; padding:.32rem 1rem; letter-spacing:.06em; box-shadow:0 0 16px rgba(34,227,208,.15);
}
@keyframes pop{ from{opacity:0; transform:scale(.85) translateY(12px);} to{opacity:1; transform:none;} }
@keyframes gradePop{ 0%{opacity:0; transform:scale(.4) rotate(-8deg);} 100%{opacity:1; transform:none;} }
</style>
"""

# ไอคอน SVG สำหรับการ์ด metric (เส้นนีออน)
ICON_DATA = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M3 10 12 3 21 10v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>'
    '<path d="M9 20v-6h6v6"/></svg>'
)
ICON_PRICE = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
)
ICON_FEATURES = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="3"/>'
    '<path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/></svg>'
)
_SPARKLINE = (
    '<svg class="gcard-spark" width="58" height="26" viewBox="0 0 58 26" fill="none">'
    '<polyline points="2,22 14,16 24,19 36,8 46,11 56,3" stroke="#4ADE80" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'style="filter:drop-shadow(0 0 5px rgba(74,222,128,.6))"/></svg>'
)

# จานสีกราฟ — นีออนฟ้า/เขียว/ม่วง
PLOT_SEQ = ["#22E3D0", "#38BDF8", "#4ADE80", "#A78BFA", "#F472B6", "#FBBF24"]
PLOT_SCALE = ["#F472B6", "#1E2A3D", "#38BDF8", "#22E3D0"]


def style_fig(fig):
    """ปรับ Plotly figure ให้เข้าธีม dark นีออน"""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans Thai, sans-serif", color="#DCE7F4", size=13),
        colorway=PLOT_SEQ,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="rgba(120,165,210,.12)", zerolinecolor="rgba(120,165,210,.25)")
    fig.update_yaxes(gridcolor="rgba(120,165,210,.12)", zerolinecolor="rgba(120,165,210,.25)")
    return fig


def grade_for(r2: float):
    """แปลงค่า R² เป็น (คะแนน 0-100, เกรด, สี, ข้อความ) สำหรับโหมดเกม"""
    score = max(0.0, r2) * 100
    if score >= 95:
        return score, "S", "#5EEAD4", "สุดยอด! โมเดลแม่นยำระดับเทพ"
    if score >= 90:
        return score, "A", "#4ADE80", "ยอดเยี่ยม โมเดลทำงานได้ดีมาก"
    if score >= 80:
        return score, "B", "#38BDF8", "ดี — ลองปรับค่าเพิ่มอีกนิด"
    if score >= 70:
        return score, "C", "#FBBF24", "พอใช้ ยังพัฒนาได้อีก"
    return score, "D", "#F472B6", "ลองปรับพลังโมเดลใหม่ดูสิ"


def score_card(score: float, grade: str, color: str, msg: str, best: float) -> None:
    """การ์ดคะแนนแบบเกม: เกรดใหญ่ + คะแนน + สถิติสูงสุด"""
    st.markdown(
        f"""
        <div class="score-card">
          <div class="sc-label">คะแนนความแม่นยำ</div>
          <div class="grade" style="color:{color}; text-shadow:0 0 28px {color}88">{grade}</div>
          <div class="score-num">{score:.1f}<span>/ 100</span></div>
          <div class="sc-msg">{msg}</div>
          <div class="sc-best">🏆 สถิติสูงสุด {best:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glow_metric(icon_svg: str, label: str, value: str) -> str:
    """คืน HTML การ์ด metric เรืองแสง (ไอคอน + sparkline + ค่า)"""
    return f"""
    <div class="gcard">
      <div class="gcard-top">
        <div class="gcard-ico">{icon_svg}</div>
        {_SPARKLINE}
      </div>
      <div class="gcard-label">{label}</div>
      <div class="gcard-value">{value}</div>
    </div>
    """


def _theme_control() -> str:
    """แสดง Toggle เปลี่ยนธีมด้านซ้ายบน — ป้ายเปลี่ยนตามธีมที่เลือก"""
    # อ่านสถานะปัจจุบันก่อนสร้าง widget เพื่อทำ label แบบ dynamic
    is_day = st.session_state.get("day_dream", False)
    label = "☀️ Day Dream" if is_day else "🌙 Dark"
    left, _ = st.columns([2, 5])
    with left:
        st.toggle(
            label,
            key="day_dream",
            help="เปิด = โทนสว่าง Day Dream · ปิด = โทนเข้ม Dark",
        )
    is_day = st.session_state.get("day_dream", False)
    return "Day Dream" if is_day else "Dark"


def inject_style() -> None:
    """ฉีด CSS + โลโก้ของระบบดีไซน์ — เรียกที่บนสุดของทุกหน้า"""
    theme = _theme_control()
    root_vars = _THEMES.get(theme, _DARK_VARS)
    css = _CSS.replace("__GRAIN__", _GRAIN).replace("__ROOT__", root_vars)
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(_AURORA, unsafe_allow_html=True)
    st.markdown(_EMBLEM, unsafe_allow_html=True)


def page_header(title: str, kicker: str = "", subtitle: str = "") -> None:
    """หัวเรื่องแบบ editorial: kicker mono + ชื่อใหญ่ไล่เฉด + คำโปรย + เส้นเรืองแสง"""
    parts = ['<div class="eh">']
    if kicker:
        parts.append(f'<div class="kicker">{kicker}</div>')
    parts.append(f'<h1 class="eh-title">{title}</h1>')
    if subtitle:
        parts.append(f'<div class="eh-sub">{subtitle}</div>')
    parts.append('<div class="rule"></div></div>')
    st.markdown("".join(parts), unsafe_allow_html=True)
