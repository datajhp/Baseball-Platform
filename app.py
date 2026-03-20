"""
부산갈매기 ⚾ 롯데 자이언츠 팬 플랫폼
"""
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from datetime import datetime as dt
import uuid, hashlib, json, re
import xml.etree.ElementTree as ET

today = datetime.date.today()

st.set_page_config(
    layout="wide",
    page_title="부산갈매기 · 롯데 자이언츠",
    page_icon="⚾",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════
#  GLOBAL CSS — 토스 디자인, 명시적 색상 지정
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* ── 리셋 & 기반 ── */
html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #191F28 !important;
}
*, *::before, *::after { box-sizing: border-box; }
.stApp { background: #F2F4F7 !important; }
.main .block-container { padding: 1.5rem 2rem 5rem !important; max-width: 1440px !important; }
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── 탭 ── */
div[data-testid="stTabs"] > div:first-child > div[role="tablist"] {
    background: #fff !important;
    border-radius: 18px !important; padding: 7px !important; gap: 4px !important;
    border: 1px solid #E5E8EB !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.06) !important;
    margin-bottom: 28px !important;
}
div[data-testid="stTabs"] button[role="tab"] {
    border-radius: 13px !important; padding: 10px 22px !important;
    font-size: 15px !important; font-weight: 600 !important;
    color: #4E5968 !important; border: none !important;
    background: transparent !important; transition: all .25s !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #3182F6 !important; color: #fff !important;
    box-shadow: 0 3px 12px rgba(49,130,246,.35) !important;
}
div[data-testid="stTabs"] div[role="tabpanel"] { border: none !important; padding: 0 !important; }

/* ── Streamlit 마크다운 텍스트만 명시 (전역 금지) ── */
.stMarkdown p { color: #191F28; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #191F28; }

/* ── 일반 버튼 ── */
div[data-testid="stButton"] > button {
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; letter-spacing: -.1px !important;
    transition: all .2s !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: #3182F6 !important; border: none !important;
    color: #ffffff !important;
}
div[data-testid="stButton"] > button[kind="primary"] p,
div[data-testid="stButton"] > button[kind="primary"] span {
    color: #ffffff !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: #ffffff !important; border: 2px solid #E5E8EB !important;
    color: #333D4B !important;
}
div[data-testid="stButton"] > button[kind="secondary"] p,
div[data-testid="stButton"] > button[kind="secondary"] span {
    color: #333D4B !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,.13) !important;
}

/* ── 링크 버튼 — 완전 재정의 ── */
div[data-testid="stLinkButton"] { display: block !important; }
div[data-testid="stLinkButton"] a {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 18px !important;
    background: #3182F6 !important;
    color: #ffffff !important;
    text-decoration: none !important;
    border: none !important;
    transition: all .2s !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
div[data-testid="stLinkButton"] a:hover {
    background: #1a6ee8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(49,130,246,.35) !important;
}
div[data-testid="stLinkButton"] a p,
div[data-testid="stLinkButton"] a span,
div[data-testid="stLinkButton"] a * {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ── 인풋 ── */
div[data-testid="stTextInput"] input {
    border: 2px solid #E5E8EB !important; border-radius: 12px !important;
    font-size: 14px !important; font-weight: 500 !important;
    color: #191F28 !important; background: #fff !important;
    padding: 10px 14px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 4px rgba(49,130,246,.12) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] p {
    color: #4E5968 !important; font-weight: 600 !important; font-size: 13px !important;
}
div[data-testid="stTextArea"] textarea {
    border: 2px solid #E5E8EB !important; border-radius: 12px !important;
    font-size: 14px !important; color: #191F28 !important; background: #fff !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 4px rgba(49,130,246,.12) !important;
}
div[data-testid="stTextArea"] label, div[data-testid="stTextArea"] p {
    color: #4E5968 !important; font-weight: 600 !important; font-size: 13px !important;
}

/* ── 셀렉트박스 ── */
div[data-testid="stSelectbox"] label, div[data-testid="stSelectbox"] p {
    color: #4E5968 !important; font-weight: 600 !important; font-size: 13px !important;
}
div[data-testid="stSelectbox"] > div > div {
    border: 2px solid #E5E8EB !important; border-radius: 12px !important;
    background: #fff !important; color: #191F28 !important;
}

/* ── 라디오 버튼 ── */
div[data-testid="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    color: #191F28 !important; font-weight: 700 !important; font-size: 15px !important;
    margin-bottom: 10px !important;
}
div[data-testid="stRadio"] > div {
    display: flex !important; flex-direction: column !important; gap: 8px !important;
}
div[data-testid="stRadio"] > div > label {
    background: #F8F9FA !important;
    border: 2px solid #E5E8EB !important;
    border-radius: 14px !important; padding: 14px 16px !important;
    cursor: pointer !important; transition: all .2s !important;
    display: flex !important; align-items: center !important; gap: 10px !important;
    margin: 0 !important; min-height: 52px !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #3182F6 !important; background: #EFF6FF !important;
}
/* 라디오 선택지 텍스트 — 명시적으로 어두운 색상 */
div[data-testid="stRadio"] > div > label > div,
div[data-testid="stRadio"] > div > label > div > p,
div[data-testid="stRadio"] > div > label > div > span {
    color: #191F28 !important; font-size: 15px !important;
    font-weight: 600 !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #EFF6FF !important; border-color: #3182F6 !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) > div,
div[data-testid="stRadio"] > div > label:has(input:checked) > div > p,
div[data-testid="stRadio"] > div > label:has(input:checked) > div > span {
    color: #1D4ED8 !important;
}
div[data-testid="stRadio"] input[type="radio"] { accent-color: #3182F6 !important; }

/* ── 알림 ── */
div[data-testid="stAlert"] { border-radius: 12px !important; }
div[data-testid="stAlert"] p { color: inherit !important; }

/* ── container border (st.container(border=True)) ── */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 2px solid #E5E8EB !important;
    border-radius: 20px !important;
    padding: 24px !important;
    background: #ffffff !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.04) !important;
}

/* ── 애니메이션 ── */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
.ldot {
    display: inline-block; width: 7px; height: 7px;
    border-radius: 50%; background: #EF4444;
    animation: blink 1.4s infinite;
}

/* ══════════════════════════════════════
   반응형 레이아웃 — Streamlit 컬럼 재배치
   ══════════════════════════════════════ */

/* 1160px 이하: 전체 컬럼 너비를 균등하게 */
@media (max-width: 1160px) {
    /* 홈 3컬럼 → 좌우 컬럼을 상대적으로 넓게 */
    .main .block-container { padding: 1.5rem 1rem 5rem !important; }

    /* Streamlit이 flex로 렌더링하는 columns 컨테이너 */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }

    /* 첫 번째(순위) 컬럼 — 전체 너비로 */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* 가운데(경기+뉴스) 컬럼 — 60% */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) {
        min-width: 60% !important;
        flex: 1 1 60% !important;
    }

    /* 오른쪽(하이라이트+티켓) 컬럼 — 38% */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) {
        min-width: 38% !important;
        flex: 1 1 38% !important;
    }
}

/* 900px 이하: 2컬럼으로 변환 */
@media (max-width: 900px) {
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }
}

/* 640px 이하: 완전 1컬럼 */
@media (max-width: 640px) {
    .main .block-container { padding: 1rem 0.75rem 4rem !important; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
        width: 100% !important;
    }
    /* iframe 카드도 작게 */
    iframe { min-height: unset !important; }
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
#  컴포넌트 CSS (HTML 내부 스타일)
# ──────────────────────────────────────────
COMPONENT_CSS = """
<style>
/* ── 카드 ── */
.T-card {
    background: #fff; border-radius: 20px; padding: 24px;
    border: 1px solid #F0F2F5; box-shadow: 0 2px 12px rgba(0,0,0,.04);
    margin-bottom: 20px;
}
.T-card-title {
    font-size: 17px !important; font-weight: 800 !important; color: #191F28 !important;
    margin: 0 0 18px 0 !important; display: flex; align-items: center; gap: 8px;
    letter-spacing: -.4px;
}

/* ── KBO 순위표 ── */
.T-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.T-table th {
    background: #F8F9FB; color: #8B95A1 !important; font-weight: 700;
    padding: 8px 4px; text-align: center; font-size: 10px;
    letter-spacing: .2px; border-bottom: 2px solid #ECEEF2; white-space: nowrap; overflow: hidden;
}
.T-table td {
    padding: 10px 4px; text-align: center;
    color: #333D4B !important; border-bottom: 1px solid #F5F6F8; font-size: 12px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.T-table tr.HL td {
    background: #EFF6FF !important; color: #1D4ED8 !important; font-weight: 800 !important;
}
.T-table tr:last-child td { border-bottom: none; }
.RN {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%; font-size: 11px; font-weight: 800;
}
.RN1 { background: #FEF3C7; color: #D97706 !important; }
.RN2 { background: #F1F5F9; color: #64748B !important; }
.RN3 { background: #FFF3E0; color: #C2590A !important; }
.RNn { background: #F2F4F7; color: #6B7684 !important; }

/* ── 경기 카드 ── */
.G-card {
    background: #fff; border: 1.5px solid #ECEEF2; border-radius: 16px;
    padding: 16px 20px; margin-bottom: 10px;
    transition: border-color .2s, box-shadow .2s;
}
.G-card.lotte { border-left: 4px solid #EF4444 !important; }
.G-team { font-size: 16px !important; font-weight: 900 !important; color: #191F28 !important; }
.G-score {
    background: #F2F4F7; border-radius: 10px;
    padding: 8px 20px; font-size: 22px; font-weight: 900;
    color: #191F28 !important; letter-spacing: 5px;
}
.G-meta { font-size: 12px !important; color: #8B95A1 !important; font-weight: 500; }
.S-live { display:inline-flex;align-items:center;gap:5px;padding:4px 11px;border-radius:999px;font-size:11px;font-weight:700;background:#FEF2F2;color:#DC2626!important;border:1.5px solid #FECACA; }
.S-sched { display:inline-flex;align-items:center;gap:5px;padding:4px 11px;border-radius:999px;font-size:11px;font-weight:700;background:#EFF6FF;color:#1D4ED8!important;border:1.5px solid #BFDBFE; }
.S-done { display:inline-flex;align-items:center;gap:5px;padding:4px 11px;border-radius:999px;font-size:11px;font-weight:700;background:#F0FDF4;color:#15803D!important;border:1.5px solid #BBF7D0; }
.S-cancel { display:inline-flex;align-items:center;gap:5px;padding:4px 11px;border-radius:999px;font-size:11px;font-weight:700;background:#F9FAFB;color:#6B7684!important;border:1.5px solid #E5E8EB; }

/* ── 뉴스 ── */
.N-item { padding:14px 0;border-bottom:1px solid #F2F4F7;display:flex;gap:12px;align-items:flex-start; }
.N-item:last-child { border-bottom:none; }
.N-num { min-width:22px;height:22px;border-radius:6px;background:#F2F4F7;color:#8B95A1!important;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-top:2px; }
.N-title a { font-size:14px !important;font-weight:600 !important;color:#191F28 !important;text-decoration:none;line-height:1.6; }
.N-title a:hover { color:#3182F6 !important; }
.N-press { font-size:11px !important;color:#B0B8C1 !important;font-weight:500;margin-top:3px; }

/* ── YouTube 카드 ── */
.YT-card {
    display:flex;gap:12px;background:#fff;border:1.5px solid #ECEEF2;
    border-radius:14px;padding:12px;margin-bottom:10px;text-decoration:none;
    transition:all .2s;
}
.YT-card:hover { border-color:#BFDBFE;box-shadow:0 4px 16px rgba(49,130,246,.1);transform:translateY(-1px); }
.YT-thumb { width:88px;height:54px;object-fit:cover;border-radius:8px;flex-shrink:0; }
.YT-ttl { font-size:12px !important;font-weight:700 !important;color:#191F28 !important;line-height:1.5;margin-bottom:4px;
          display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden; }
.YT-meta { font-size:10px !important;color:#8B95A1 !important; }

/* ── 투표 바 ── */
.VB-wrap { display:flex;height:56px;border-radius:14px;overflow:hidden;background:#F2F4F7;margin:8px 0; }
.VB-l { background:linear-gradient(90deg,#991B1B,#EF4444);display:flex;align-items:center;justify-content:center;color:#fff !important;font-weight:800;font-size:14px; }
.VB-r { background:linear-gradient(90deg,#1E40AF,#3B82F6);display:flex;align-items:center;justify-content:center;color:#fff !important;font-weight:800;font-size:14px;flex:1; }

/* ── 통계 박스 ── */
.ST-box { background:#F8F9FA;border-radius:14px;padding:18px;text-align:center; }
.ST-val { font-size:28px !important;font-weight:900 !important;color:#191F28 !important;line-height:1; }
.ST-lbl { font-size:12px !important;color:#8B95A1 !important;font-weight:600;margin-top:6px; }

/* ── 게시판 목록 ── */
.P-row {
    display:flex;align-items:center;gap:12px;padding:15px 18px;
    background:#fff;border:1.5px solid #ECEEF2;border-radius:14px;margin-bottom:8px;
    transition:all .2s;cursor:pointer;
}
.P-row:hover { border-color:#BFDBFE;box-shadow:0 4px 16px rgba(49,130,246,.1);transform:translateY(-1px); }
.P-cat { display:inline-flex;align-items:center;padding:3px 10px;border-radius:8px;font-size:11px;font-weight:800;white-space:nowrap; }
.P-cat.자유 { background:#EFF6FF;color:#1D4ED8 !important; }
.P-cat.응원 { background:#FEF2F2;color:#DC2626 !important; }
.P-cat.분석 { background:#F0FDF4;color:#15803D !important; }
.P-cat.질문 { background:#FFF7ED;color:#C2590A !important; }
.P-cat.거래 { background:#F5F3FF;color:#6D28D9 !important; }
.P-title { font-size:14px !important;font-weight:600 !important;color:#191F28 !important;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }
.P-meta { display:flex;gap:10px;font-size:11px !important;color:#8B95A1 !important;font-weight:500;white-space:nowrap; }

/* ── 게시글 상세 ── */
.POST-wrap { background:#fff;border-radius:20px;padding:32px;border:1.5px solid #ECEEF2;margin-bottom:16px; }
.POST-title { font-size:22px !important;font-weight:800 !important;color:#191F28 !important;margin:12px 0 14px;letter-spacing:-.5px;line-height:1.4; }
.POST-meta { display:flex;gap:16px;font-size:13px !important;color:#8B95A1 !important;flex-wrap:wrap;margin-bottom:24px; }
.POST-meta strong { color:#4E5968 !important; }
.POST-body { font-size:15px !important;color:#333D4B !important;line-height:1.9;white-space:pre-wrap;word-break:break-word; }
.CMT-item { padding:14px 0;border-bottom:1px solid #F5F6F8; }
.CMT-item:last-child { border-bottom:none; }
.CMT-author { font-size:13px !important;font-weight:700 !important;color:#333D4B !important; }
.CMT-time { font-size:11px !important;color:#B0B8C1 !important;margin-left:8px; }
.CMT-body { font-size:14px !important;color:#4E5968 !important;line-height:1.7;margin-top:5px;word-break:break-word; }

/* ── 공통 ── */
.VTAG { display:inline-flex;align-items:center;background:#F2F4F7;color:#333D4B !important;border-radius:8px;padding:5px 11px;font-size:12px;font-weight:700;margin:3px; }
.DIVIDER { border:none;border-top:1px solid #ECEEF2;margin:16px 0; }
.EMPTY { text-align:center;padding:40px 0; }
.EMPTY-i { font-size:40px;margin-bottom:10px; }
.EMPTY-t { font-size:15px !important;font-weight:700 !important;color:#4E5968 !important;margin-bottom:5px; }
.EMPTY-s { font-size:13px !important;color:#8B95A1 !important; }

/* ── 히어로 ── */
.HERO {
    background: linear-gradient(135deg, #0C2461 0%, #1E3799 45%, #2563EB 100%);
    border-radius: 28px; padding: 44px 52px; margin-bottom: 32px;
    position: relative; overflow: hidden;
    box-shadow: 0 16px 48px rgba(12,36,97,.35);
}
.HERO::before {
    content: "⚾"; position:absolute; right:52px; top:50%;
    transform:translateY(-50%); font-size:130px; opacity:.08; line-height:1;
}
.HERO-badge {
    display:inline-flex;align-items:center;gap:6px;
    background:rgba(255,255,255,.15);color:rgba(255,255,255,.9) !important;
    padding:5px 14px;border-radius:999px;font-size:13px;font-weight:600;
    margin-bottom:14px;border:1px solid rgba(255,255,255,.2);
}
.HERO-h1 { color:#fff !important;font-size:36px !important;font-weight:900 !important;margin:0 0 8px !important;letter-spacing:-1px !important; }
.HERO-sub { color:rgba(255,255,255,.65) !important;font-size:15px !important;margin:0 !important;font-weight:500 !important; }
.HERO-live {
    display:inline-flex;align-items:center;gap:7px;
    background:rgba(239,68,68,.2);color:#FCA5A5 !important;
    padding:5px 13px;border-radius:999px;font-size:12px;font-weight:700;
    margin-top:14px;border:1px solid rgba(239,68,68,.35);
}
</style>
"""
st.markdown(COMPONENT_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  Supabase
# ══════════════════════════════════════════
@st.cache_resource
def get_sb():
    try:
        from supabase import create_client
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except Exception:
        return None

sb = get_sb()

for k, v in {"bv": "list", "pid": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.koreabaseball.com/",
}

# ══════════════════════════════════════════
#  팀 로고 — JS 이벤트 핸들러 없는 순수 HTML
# ══════════════════════════════════════════
# 네이버 스포츠 CDN (안정적, CORS 없음)
TEAM_LOGO = {
    "LG":  "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_LG.png",
    "SSG": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_SK.png",
    "두산": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_OB.png",
    "삼성": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_SS.png",
    "NC":  "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_NC.png",
    "롯데": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_LT.png",
    "키움": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_WO.png",
    "KT":  "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_KT.png",
    "KIA": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_HT.png",
    "한화": "https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/emblem/regular/fixed/emblem_HH.png",
}

def team_logo_html(team_name, size=52):
    url = TEAM_LOGO.get(team_name, "")
    if url:
        # onerror 없이 단순 img 태그
        return f'<img src="{url}" alt="{team_name}" width="{size}" height="{size}" style="object-fit:contain">'
    # 로고 없으면 텍스트 뱃지
    return f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#F2F4F7;display:inline-flex;align-items:center;justify-content:center;font-size:{size//4}px;font-weight:800;color:#6B7684">{team_name[:2]}</div>'


# ══════════════════════════════════════════
#  스크래핑 함수
# ══════════════════════════════════════════
@st.cache_data(ttl=300)
def get_standings():
    try:
        res = requests.get(
            "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx",
            headers=HDR, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.tData")
        if not table:
            return None
        df = pd.read_html(str(table))[0]
        if "팀명" in df.columns:
            df = df.rename(columns={"팀명": "팀"})
        cols = [c for c in ["순위","팀","승","패","무","승률","게임차"] if c in df.columns]
        return df[cols].reset_index(drop=True)
    except Exception:
        return None


@st.cache_data(ttl=60)
def get_today_games():
    """
    KBO 오늘 경기 — GetKboGameList API (확인된 필드명 사용)
    AWAY_NM, HOME_NM, T_SCORE_CN, B_SCORE_CN, GAME_STATE_SC, G_TM, S_NM
    """
    today_str = today.strftime("%Y%m%d")
    games = []

    # ── 소스 1: GetKboGameList (KBO 공식 메인 API)
    try:
        url = "https://www.koreabaseball.com/ws/Main.asmx/GetKboGameList"
        payload = {"leId": "1", "srId": "1", "date": today_str}
        res = requests.post(
            url, data=payload,
            headers={
                **HDR,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.koreabaseball.com",
                "Referer": "https://www.koreabaseball.com/",
            },
            timeout=10)
        if res.status_code == 200:
            data = res.json()
            for g in data.get("game", []):
                away  = g.get("AWAY_NM", "")
                home  = g.get("HOME_NM", "")
                vs    = str(g.get("T_SCORE_CN", ""))
                hs    = str(g.get("B_SCORE_CN", ""))
                sc    = str(g.get("GAME_STATE_SC", ""))
                time_s = g.get("G_TM", "")[:5]
                stad   = g.get("S_NM", "")
                cancel = g.get("CANCEL_SC_NM", "")

                score = f"{vs}:{hs}" if vs not in ("","None","0") or hs not in ("","None","0") else "vs"
                # 점수가 실제로 있는지 확인 (경기 전은 0:0이라도 표시 안 함)
                if sc == "0" or sc == "":  # 경기 전
                    score = "vs"
                    state = ""
                elif sc == "1":            # 진행중
                    score = f"{vs}:{hs}"
                    state = "진행중"
                elif sc == "2":            # 지연
                    score = f"{vs}:{hs}"
                    state = "지연"
                elif sc == "3":            # 종료
                    score = f"{vs}:{hs}"
                    state = "종료"
                else:
                    score = "vs"
                    state = ""

                if "취소" in cancel or "우천" in cancel:
                    state = "취소"
                    score = "vs"

                if away and home:
                    games.append({
                        "away": away, "home": home, "score": score,
                        "time": time_s, "stadium": stad, "state": state,
                        "is_lotte": "롯데" in [away, home],
                        "win_pit":  g.get("W_PIT_P_NM", ""),
                        "lose_pit": g.get("L_PIT_P_NM", ""),
                        "save_pit": g.get("SV_PIT_P_NM", ""),
                        "away_sp":  g.get("T_PIT_P_NM", ""),
                        "home_sp":  g.get("B_PIT_P_NM", ""),
                        "inning":   g.get("GAME_INN_NO", ""),
                        "game_id":  g.get("G_ID", ""),
                    })
    except Exception:
        pass

    # ── 소스 2: GetScheduleList (srId=1 정규, srId=0 시범)
    if not games:
        for sr_id in ["1", "0"]:
            try:
                res = requests.post(
                    "https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList",
                    data={"leId": "1", "srId": sr_id, "date": today_str},
                    headers={
                        **HDR,
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Requested-With": "XMLHttpRequest",
                        "Origin": "https://www.koreabaseball.com",
                    },
                    timeout=10)
                if res.status_code != 200:
                    continue
                data = res.json()
                for g in data.get("game", []):
                    away  = g.get("AWAY_NM", g.get("awayTeamName", ""))
                    home  = g.get("HOME_NM", g.get("homeTeamName", ""))
                    vs    = str(g.get("T_SCORE_CN", g.get("awayScore", "")))
                    hs    = str(g.get("B_SCORE_CN", g.get("homeScore", "")))
                    sc    = str(g.get("GAME_STATE_SC", g.get("status", "")))
                    time_s = g.get("G_TM", g.get("gameTime", ""))[:5]
                    stad   = g.get("S_NM", g.get("stadiumName", ""))
                    if sc == "3": state, score = "종료", f"{vs}:{hs}"
                    elif sc == "1": state, score = "진행중", f"{vs}:{hs}"
                    else: state, score = "", "vs"
                    if away and home:
                        games.append({
                            "away": away, "home": home, "score": score,
                            "time": time_s, "stadium": stad, "state": state,
                            "is_lotte": "롯데" in [away, home],
                        })
                if games:
                    break
            except Exception:
                continue

    # ── 소스 3: HTML 파싱 최후 수단
    if not games:
        try:
            url = f"https://sports.news.naver.com/kbaseball/schedule/index?date={today_str}"
            res = requests.get(url, headers={**HDR, "Referer": "https://sports.news.naver.com/"}, timeout=12)
            soup = BeautifulSoup(res.text, "html.parser")
            kbo_teams = ["롯데","삼성","LG","두산","KT","SSG","한화","NC","KIA","키움"]
            stadiums  = ["사직","잠실","수원","대전","고척","창원","광주","대구","인천","포항","청주"]
            seen = set()
            for row in soup.select("tr, li"):
                text  = row.get_text(" ", strip=True)
                found = [t for t in kbo_teams if t in text]
                if len(found) < 2: continue
                key = f"{found[0]}{found[1]}"
                if key in seen: continue
                seen.add(key)
                sm = re.search(r'(\d+)\s*[:\-]\s*(\d+)', text)
                tm = re.search(r'(\d{1,2}:\d{2})', text)
                games.append({
                    "away": found[0], "home": found[1],
                    "score": f"{sm.group(1)}:{sm.group(2)}" if sm else "vs",
                    "time":  tm.group(1) if tm else "",
                    "stadium": next((s for s in stadiums if s in text), ""),
                    "state": "종료" if "종료" in text else "진행중" if "진행" in text else "",
                    "is_lotte": "롯데" in found,
                })
        except Exception:
            pass

    return games


@st.cache_data(ttl=300)
def get_lotte_news():
    try:
        url = "https://news.google.com/rss/search?q=롯데+자이언츠&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url, headers=HDR, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.text)
        news = []
        for item in root.findall(".//item")[:10]:
            t  = item.find("title")
            l  = item.find("link")
            s  = item.find("source")
            p  = item.find("pubDate")
            title = re.sub(r'\s*-\s*[^-]+$', '', t.text or "").strip() if t is not None else ""
            if title:
                news.append({
                    "title": title,
                    "url":   l.text or "" if l is not None else "",
                    "press": s.text or "" if s is not None else "",
                    "pub":   (p.text or "")[:16] if p is not None else "",
                })
        return news
    except Exception:
        return []


@st.cache_data(ttl=1800)
def get_youtube_highlights():
    try:
        query = "롯데+자이언츠+하이라이트"
        url   = f"https://www.youtube.com/results?search_query={query}&sp=CAI%3D"
        res   = requests.get(url, headers=HDR, timeout=15)
        res.raise_for_status()
        m = re.search(r'ytInitialData\s*=\s*({.+?});\s*</script>', res.text)
        if not m:
            return []
        data = json.loads(m.group(1))
        secs = (data.get("contents",{})
                    .get("twoColumnSearchResultsRenderer",{})
                    .get("primaryContents",{})
                    .get("sectionListRenderer",{})
                    .get("contents",[]))
        videos = []
        for sec in secs:
            for item in sec.get("itemSectionRenderer",{}).get("contents",[]):
                vr = item.get("videoRenderer",{})
                if not vr: continue
                vid   = vr.get("videoId","")
                title = (vr.get("title",{}).get("runs") or [{}])[0].get("text","")
                ch    = (vr.get("ownerText",{}).get("runs") or [{}])[0].get("text","")
                pub   = vr.get("publishedTimeText",{}).get("simpleText","")
                thumbs= vr.get("thumbnail",{}).get("thumbnails",[])
                thumb = thumbs[-1].get("url","") if thumbs else f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                if vid and title:
                    videos.append({"id":vid,"title":title,"channel":ch,"time":pub,"thumb":thumb})
                if len(videos) >= 4: return videos
        return videos
    except Exception:
        return []


# ══════════════════════════════════════════
#  DB 함수
# ══════════════════════════════════════════
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def fmt_dt(ts, mode="short"):
    if not ts: return ""
    try:
        d = dt.fromisoformat(ts.replace("Z","+00:00"))
        return d.strftime("%m.%d %H:%M") if mode=="short" else d.strftime("%Y.%m.%d %H:%M")
    except: return str(ts)[:16].replace("T"," ")

def db_posts(cat="전체"):
    if not sb: return []
    try:
        q = sb.table("lotte_posts").select("*").order("created_at",desc=True)
        if cat != "전체": q = q.eq("category", cat)
        return q.execute().data or []
    except: return []

def db_post(pid):
    if not sb: return None
    try: return sb.table("lotte_posts").select("*").eq("id",str(pid)).single().execute().data
    except: return None

def db_create_post(title, content, author, pw, cat):
    if not sb: return False
    try:
        sb.table("lotte_posts").insert({
            "id":str(uuid.uuid4()),"title":title,"content":content,
            "author":author or "익명","password":hash_pw(pw) if pw else "",
            "category":cat,"views":0,"likes":0,
        }).execute()
        return True
    except Exception as e:
        st.error(f"등록 오류: {e}"); return False

def db_delete_post(pid, pw):
    if not sb: return False, "DB 연결 오류"
    try:
        post = db_post(pid)
        if not post: return False, "게시글을 찾을 수 없습니다."
        if post.get("password") and post["password"] != hash_pw(pw):
            return False, "비밀번호가 맞지 않습니다."
        sb.table("lotte_posts").delete().eq("id",str(pid)).execute()
        return True, ""
    except Exception as e: return False, str(e)

def db_inc_views(pid):
    if not sb: return
    try:
        p = db_post(pid)
        if p: sb.table("lotte_posts").update({"views":p.get("views",0)+1}).eq("id",str(pid)).execute()
    except: pass

def db_like(pid):
    if not sb: return 0
    try:
        p = db_post(pid)
        if p:
            nl = p.get("likes",0)+1
            sb.table("lotte_posts").update({"likes":nl}).eq("id",str(pid)).execute()
            return nl
    except: return 0

def db_comments(pid):
    if not sb: return []
    try: return sb.table("lotte_comments").select("*").eq("post_id",str(pid)).order("created_at").execute().data or []
    except: return []

def db_add_comment(pid, author, content):
    if not sb: return False
    try:
        sb.table("lotte_comments").insert({"id":str(uuid.uuid4()),"post_id":str(pid),"author":author or "익명","content":content}).execute()
        return True
    except: return False

def db_today_votes():
    if not sb: return pd.DataFrame()
    try:
        res = sb.table("vote_predictions").select("*").eq("vote_date",today.isoformat()).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except: return pd.DataFrame()

def db_add_vote(nick, team):
    if not sb: return False
    try:
        sb.table("vote_predictions").insert({"id":str(uuid.uuid4()),"nickname":nick,"selected_team":team,"vote_date":today.isoformat()}).execute()
        return True
    except: return False


# ══════════════════════════════════════════
#  헬퍼 — 경기 상태 뱃지
# ══════════════════════════════════════════
#  경기카드 렌더 함수
# ══════════════════════════════════════════
def render_games_horizontal(games, show_pitcher=True):
    """경기 카드 HTML 반환 — components.v1.html로 렌더링"""
    if not games:
        return '<div style="text-align:center;padding:28px 0;color:#8B95A1;font-family:Pretendard,sans-serif"><div style="font-size:36px;margin-bottom:8px">🌙</div><div style="font-size:15px;font-weight:700;color:#4E5968;margin-bottom:4px">오늘은 경기가 없어요</div><div style="font-size:13px">내일을 기대해봐요!</div></div>'

    cards = ""
    for g in games:
        aw, hm = g["away"], g["home"]
        is_l   = g["is_lotte"]
        bdg    = state_badge_inline(g["state"], g["time"])
        aw_url = TEAM_LOGO.get(aw, "")
        hm_url = TEAM_LOGO.get(hm, "")
        aw_img = f'<img src="{aw_url}" width="48" height="48" style="object-fit:contain;display:block">' if aw_url else f'<div style="width:48px;height:48px;border-radius:50%;background:#F2F4F7;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#6B7684">{aw[:2]}</div>'
        hm_img = f'<img src="{hm_url}" width="48" height="48" style="object-fit:contain;display:block">' if hm_url else f'<div style="width:48px;height:48px;border-radius:50%;background:#F2F4F7;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#6B7684">{hm[:2]}</div>'
        stad = g.get("stadium","")

        if ":" in g["score"]:
            p = g["score"].split(":")
            av, hv = int(p[0]), int(p[1])
            ac = "#DC2626" if av>hv else "#9CA3AF" if av<hv else "#191F28"
            hc = "#DC2626" if hv>av else "#9CA3AF" if hv<av else "#191F28"
            score_html = f'<span style="font-size:24px;font-weight:900;color:{ac};font-family:Pretendard,sans-serif">{av}</span><span style="font-size:16px;color:#E5E7EB;margin:0 4px">:</span><span style="font-size:24px;font-weight:900;color:{hc};font-family:Pretendard,sans-serif">{hv}</span>'
        else:
            score_html = '<span style="font-size:13px;color:#D1D5DB;font-weight:600">vs</span>'

        pit_html = ""
        if show_pitcher and g["state"] == "종료":
            rows = ""
            for nm, val, col in [("승", g.get("win_pit",""),"#15803D"),("패", g.get("lose_pit",""),"#DC2626"),("세", g.get("save_pit",""),"#1D4ED8")]:
                if val:
                    rows += f'<span style="font-size:10px;color:{col};font-weight:700;font-family:Pretendard,sans-serif">{nm} {val}</span>'
            if rows:
                pit_html = f'<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:8px">{rows}</div>'
        elif show_pitcher:
            sp = g.get("away_sp",""); hp = g.get("home_sp","")
            if sp or hp:
                pit_html = f'<div style="font-size:10px;color:#9CA3AF;margin-top:6px;font-family:Pretendard,sans-serif">{sp} vs {hp}</div>'

        border = "border:2.5px solid #EF4444;box-shadow:0 4px 20px rgba(239,68,68,.15)" if is_l else "border:1.5px solid #ECEEF2"
        cards += f'''
<div style="background:#fff;border-radius:18px;padding:16px 12px;{border};min-width:155px;flex:1;max-width:210px;text-align:center;font-family:Pretendard,sans-serif">
  <div style="font-size:10px;color:#9CA3AF;font-weight:600;margin-bottom:5px">{"🏟 "+stad if stad else "&nbsp;"}</div>
  <div style="margin-bottom:8px">{bdg}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:8px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1">
      {aw_img}
      <span style="font-size:11px;font-weight:800;color:#191F28;margin-top:2px">{aw}</span>
    </div>
    <div style="min-width:52px;text-align:center">{score_html}</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1">
      {hm_img}
      <span style="font-size:11px;font-weight:800;color:#191F28;margin-top:2px">{hm}</span>
    </div>
  </div>
  {pit_html}
</div>'''
    return f'<div style="display:flex;gap:10px;overflow-x:auto;padding-bottom:8px;padding-right:4px">{cards}</div>'


def render_lotte_game_big(g):
    aw, hm  = g["away"], g["home"]
    bdg     = state_badge_inline(g["state"], g["time"])
    aw_url  = TEAM_LOGO.get(aw, "")
    hm_url  = TEAM_LOGO.get(hm, "")
    aw_img  = f'<img src="{aw_url}" width="76" height="76" style="object-fit:contain;display:block">' if aw_url else f'<div style="width:76px;height:76px;background:#F2F4F7;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;color:#6B7684">{aw[:2]}</div>'
    hm_img  = f'<img src="{hm_url}" width="76" height="76" style="object-fit:contain;display:block">' if hm_url else f'<div style="width:76px;height:76px;background:#F2F4F7;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;color:#6B7684">{hm[:2]}</div>'
    stad    = g.get("stadium","")

    if ":" in g["score"]:
        p = g["score"].split(":")
        av, hv = int(p[0]), int(p[1])
        ac = "#DC2626" if av>hv else "#9CA3AF" if av<hv else "#191F28"
        hc = "#DC2626" if hv>av else "#9CA3AF" if hv<av else "#191F28"
        ascore = f'<div style="font-size:46px;font-weight:900;color:{ac};line-height:1;font-family:Pretendard,sans-serif">{av}</div>'
        hscore = f'<div style="font-size:46px;font-weight:900;color:{hc};line-height:1;font-family:Pretendard,sans-serif">{hv}</div>'
    else:
        ascore = '<div style="font-size:28px;font-weight:300;color:#D1D5DB">-</div>'
        hscore = '<div style="font-size:28px;font-weight:300;color:#D1D5DB">-</div>'

    pit_rows = ""
    if g["state"] == "종료":
        for label, val, col in [("승리투수",g.get("win_pit",""),"#15803D"),("패전투수",g.get("lose_pit",""),"#DC2626"),("세이브",g.get("save_pit",""),"#1D4ED8")]:
            if val:
                pit_rows += f'<div style="display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #F5F6F8;font-family:Pretendard,sans-serif"><span style="font-size:12px;color:#8B95A1;font-weight:600">{label}</span><span style="font-size:14px;font-weight:800;color:{col}">{val}</span></div>'
    else:
        for label, val in [("원정 선발",g.get("away_sp","")),("홈 선발",g.get("home_sp",""))]:
            if val:
                pit_rows += f'<div style="display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #F5F6F8;font-family:Pretendard,sans-serif"><span style="font-size:12px;color:#8B95A1;font-weight:600">{label}</span><span style="font-size:14px;font-weight:800;color:#333D4B">{val}</span></div>'

    pit_section = f'<div style="background:#F8F9FA;border-radius:14px;overflow:hidden;margin-top:18px">{pit_rows}</div>' if pit_rows else ""

    return f'''
<div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:20px;padding:28px 20px;font-family:Pretendard,sans-serif">
  <div style="text-align:center;margin-bottom:16px">{bdg}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:8px">
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px">
      {aw_img}
      <div style="font-size:15px;font-weight:900;color:#191F28">{aw}</div>
      <div style="font-size:11px;color:#6B7684;font-weight:600">원정</div>
      {ascore}
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:36px">
      <div style="font-size:20px;color:#D1D5DB;font-weight:300">:</div>
      <div style="font-size:10px;color:#9CA3AF;font-weight:600;text-align:center">{"🏟 "+stad if stad else ""}</div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px">
      {hm_img}
      <div style="font-size:15px;font-weight:900;color:#191F28">{hm}</div>
      <div style="font-size:11px;color:#6B7684;font-weight:600">홈</div>
      {hscore}
    </div>
  </div>
  {pit_section}
</div>'''


def state_badge_inline(state, time_s):
    """CSS 클래스 없이 완전 인라인 스타일 뱃지"""
    base = "display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;font-family:Pretendard,sans-serif"
    if state == "진행중":
        dot = '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#EF4444"></span>'
        return f'<span style="{base};background:#FEF2F2;color:#DC2626;border:1.5px solid #FECACA">{dot}진행중</span>'
    elif state == "종료":
        return f'<span style="{base};background:#F0FDF4;color:#15803D;border:1.5px solid #BBF7D0">종료</span>'
    elif state == "취소":
        return f'<span style="{base};background:#F9FAFB;color:#6B7684;border:1.5px solid #E5E8EB">취소</span>'
    else:
        t = f"⏰ {time_s}" if time_s else "예정"
        return f'<span style="{base};background:#EFF6FF;color:#1D4ED8;border:1.5px solid #BFDBFE">{t}</span>'


def card_html(title, body, extra_style=""):
    """카드 래퍼 — components.v1.html용 완전한 HTML 문서"""
    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0;padding:0;font-family:Pretendard,sans-serif}}body{{background:transparent;padding:0}}</style>
</head><body>
<div style="background:#fff;border-radius:20px;padding:22px;border:1px solid #F0F2F5;box-shadow:0 2px 12px rgba(0,0,0,.04);{extra_style}">
  <div style="font-size:17px;font-weight:800;color:#191F28;margin-bottom:18px;display:flex;align-items:center;gap:8px">{title}</div>
  {body}
</div>
</body></html>'''


# ══════════════════════════════════════════
#  히어로 배너
# ══════════════════════════════════════════
st.markdown(f"""
<div class="HERO">
    <div class="HERO-badge">⚾ 비공식 팬 플랫폼</div>
    <div class="HERO-h1">부산갈매기</div>
    <div class="HERO-sub">롯데 자이언츠 팬들이 모이는 곳 · {today.strftime('%Y년 %m월 %d일')}</div>
    <div class="HERO-live"><span class="ldot"></span>경기 정보 실시간 업데이트 중</div>
</div>
""", unsafe_allow_html=True)


def html_card(title_html, body_html, height=None):
    """
    st.components.v1.html()을 사용해 Streamlit 마크다운 sanitizer를 우회.
    ResizeObserver로 높이를 콘텐츠에 맞게 자동 조정.
    """
    css = """
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * { font-family:'Pretendard',-apple-system,BlinkMacSystemFont,sans-serif; box-sizing:border-box; margin:0; padding:0; }
    html, body { background:transparent; padding:0; margin:0; overflow:hidden; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
    a { text-decoration:none; }
    """
    card_style = "background:#fff;border-radius:20px;padding:22px 22px 28px;border:1px solid #F0F2F5;box-shadow:0 2px 12px rgba(0,0,0,.04);font-family:'Pretendard',sans-serif"
    title_style = "font-size:17px;font-weight:800;color:#191F28;margin-bottom:18px;display:flex;align-items:center;gap:8px;letter-spacing:-.4px"
    full_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>{css}</style></head>
    <body>
    <div id="card" style="{card_style}">
        <div style="{title_style}">{title_html}</div>
        {body_html}
    </div>
    <script>
    function sendHeight() {{
        var h = document.getElementById('card').getBoundingClientRect().height;
        window.parent.postMessage({{type:'streamlit:setFrameHeight', height: Math.ceil(h)+16}}, '*');
    }}
    window.addEventListener('load', sendHeight);
    if (window.ResizeObserver) {{
        new ResizeObserver(sendHeight).observe(document.getElementById('card'));
    }}
    </script>
    </body></html>"""
    # height에 여유를 충분히 줌 (잘림 방지)
    est_height = (height or 300) + 32
    st.components.v1.html(full_html, height=est_height, scrolling=False)


# ══════════════════════════════════════════
#  탭
# ══════════════════════════════════════════
t_home, t_game, t_board, t_predict = st.tabs([
    "🏠  홈", "⚾  경기", "📋  게시판", "🎯  승부예측"
])


# ════════════════════════════════════════════════════
#  🏠 홈
# ════════════════════════════════════════════════════
with t_home:
    standings   = get_standings()
    today_games = get_today_games()
    news_list   = get_lotte_news()
    highlights  = get_youtube_highlights()
    votes       = db_today_votes()

    cL, cC, cR = st.columns([1.6, 2.8, 1.8], gap="medium")

    # ─ 왼쪽
    with cL:
        # KBO 순위 — 단일 호출
        if standings is not None:
            rows = ""
            for _, r in standings.iterrows():
                rank = str(r.get("순위",""))
                is_l = "롯데" in str(r.get("팀",""))
                rc = {"1":"RN1","2":"RN2","3":"RN3"}.get(rank,"RNn")
                rows += f'<tr class="{"HL" if is_l else ""}"><td><span class="RN {rc}">{rank}</span></td><td style="text-align:left;padding-left:6px;font-weight:{"900" if is_l else "500"};color:{"#1D4ED8" if is_l else "#333D4B"}">{r.get("팀","")}</td><td style="color:{"#1D4ED8" if is_l else "#333D4B"}">{r.get("승","")}</td><td style="color:{"#1D4ED8" if is_l else "#6B7684"}">{r.get("패","")}</td><td style="color:{"#1D4ED8" if is_l else "#333D4B"}">{r.get("승률","")}</td></tr>'
            rank_body = f'<table class="T-table"><thead><tr><th>순위</th><th style="text-align:left;padding-left:6px">팀</th><th>승</th><th>패</th><th>승률</th></tr></thead><tbody>{rows}</tbody></table>'
        else:
            rank_body = '<div class="EMPTY"><div class="EMPTY-i">📡</div><div class="EMPTY-t">순위 로딩 실패</div><div class="EMPTY-s">새로고침 해주세요</div></div>'
        st.markdown(f'<div class="T-card"><div class="T-card-title">🏆 KBO 리그 순위</div>{rank_body}</div>', unsafe_allow_html=True)

        # 예측 미리보기 — 단일 호출
        tv = len(votes)
        if tv > 0:
            ln = len(votes[votes["selected_team"]=="롯데"])
            lp = round(ln/tv*100,1); op = round(100-lp,1)
            vb_l = "🔥최강 롯데🔥" if lp > 20 else ""
            vb_r = "상대팀" if op > 20 else ""
            vote_body = f'<div style="display:flex;justify-content:space-between;font-size:13px;font-weight:800;margin-bottom:8px"><span style="color:#DC2626">🔴 최강 롯데 자이언츠 {lp}%</span><span style="color:#1D4ED8">{op}% 우리에게 질 상대팀 🔵</span></div><div class="VB-wrap"><div class="VB-l" style="width:{lp}%">{vb_l}</div><div class="VB-r">{vb_r}</div></div><p style="text-align:center;font-size:12px;color:#8B95A1;margin-top:8px;font-weight:600">총 {tv}명 참여 중</p>'
        else:
            vote_body = '<div class="EMPTY" style="padding:18px 0"><div class="EMPTY-i">🗳️</div><div class="EMPTY-t">아직 예측이 없어요</div><div class="EMPTY-s">승부예측 탭에서 투표하세요!</div></div>'
        st.markdown(f'<div class="T-card"><div class="T-card-title">🎯 오늘의 예측 현황</div>{vote_body}</div>', unsafe_allow_html=True)

    # ─ 가운데
    with cC:
        # 오늘 경기 — components.v1.html로 img sanitizer 우회
        game_html = render_games_horizontal(today_games, show_pitcher=True)
        nav_a = f'<div style="margin-top:14px"><a href="https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime("%Y%m%d")}" target="_blank" style="display:block;text-align:center;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px">📋 네이버 스포츠 오늘 경기</a></div>'
        n_games = len(today_games)
        card_h = 240 if n_games == 0 else 260
        html_card(
            f'📅 오늘의 KBO 경기 <span style="font-size:13px;color:#8B95A1;font-weight:500">· {today.strftime("%m/%d")}</span>',
            game_html + nav_a,
            height=card_h
        )

        # 뉴스 — 마크다운 사용 가능 (img 없음)
        if news_list:
            news_items = ""
            for i, n in enumerate(news_list[:8], 1):
                news_items += f'<div style="padding:12px 0;border-bottom:1px solid #F2F4F7;display:flex;gap:10px"><span style="min-width:20px;height:20px;border-radius:5px;background:#F2F4F7;color:#8B95A1;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;margin-top:2px">{i}</span><div><a href="{n["url"]}" target="_blank" style="font-size:14px;font-weight:600;color:#191F28;text-decoration:none;line-height:1.5">{n["title"]}</a><div style="font-size:11px;color:#B0B8C1;margin-top:3px">{n.get("press","")} · {n.get("pub","")}</div></div></div>'
            news_body = news_items
        else:
            news_body = '<div style="text-align:center;padding:20px 0;color:#8B95A1">📡 뉴스를 불러오지 못했어요</div>'
        news_more = f'<div style="margin-top:12px"><a href="https://sports.news.naver.com/kbaseball/news/index?type=team&teamCode=LT" target="_blank" style="display:block;text-align:center;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px">🔗 네이버 스포츠 뉴스 더보기</a></div>'
        html_card("📰 롯데 자이언츠 최신 뉴스", news_body + news_more, height=540)

    # ─ 오른쪽
    with cR:
        # 하이라이트
        if highlights:
            yt_items = ""
            for v in highlights[:2]:
                vid = v["id"]
                thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                yt_items += f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank" style="display:flex;gap:12px;background:#fff;border:1.5px solid #ECEEF2;border-radius:14px;padding:12px;margin-bottom:10px;text-decoration:none"><img src="{thumb}" width="108" height="66" style="object-fit:cover;border-radius:8px;flex-shrink:0"><div><div style="font-size:13px;font-weight:700;color:#191F28;line-height:1.5;margin-bottom:4px">{v.get("title","")[:52]}</div><div style="font-size:11px;color:#8B95A1">{v.get("channel","")} · {v.get("time","")}</div></div></a>'
            hl_body = yt_items
        else:
            hl_body = '<div style="text-align:center;padding:20px 0;color:#8B95A1;font-family:Pretendard,sans-serif">🎬 영상 로딩 실패</div>'
        yt_more = '<a href="https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D" target="_blank" style="display:block;text-align:center;margin-top:4px;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif">▶ YouTube 더보기</a>'
        html_card("🎬 최신 하이라이트", hl_body + yt_more, height=400)

        # 티켓
        ticket_body = '<p style="font-size:13px;color:#6B7684;margin-bottom:14px;line-height:1.8;font-family:Pretendard,sans-serif">일반 예매 오픈<br>경기 <strong style="color:#3182F6">1주일 전 오후 2시</strong></p><a href="https://ticket.giantsclub.com/loginForm.do" target="_blank" style="display:block;text-align:center;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif;margin-bottom:8px">🎫 예매 페이지</a><a href="https://www.giantsclub.com/html/?pcode=257" target="_blank" style="display:block;text-align:center;padding:10px;background:#F2F4F7;color:#333D4B;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif">📋 시즌 일정</a>'
        html_card("🎟️ 티켓 예매", ticket_body, height=220)


# ════════════════════════════════════════════════════
#  ⚾ 경기
# ════════════════════════════════════════════════════
with t_game:
    tg   = get_today_games()
    hl   = get_youtube_highlights()
    lotg = [g for g in tg if g["is_lotte"]]

    gc1, gc2 = st.columns([3, 2], gap="medium")

    with gc1:
        # 오늘 전체 경기
        gh = render_games_horizontal(tg, show_pitcher=True)
        na = f'<div style="margin-top:14px"><a href="https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime("%Y%m%d")}" target="_blank" style="display:block;text-align:center;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif">📋 네이버 스포츠 오늘 경기</a></div>'
        html_card(f'📅 오늘 전체 경기', gh + na, height=320)

        # 롯데 오늘 경기 빅 카드
        if lotg:
            big = render_lotte_game_big(lotg[0])
            big_h = 440 if (lotg[0].get("win_pit") or lotg[0].get("away_sp")) else 360
        else:
            big = '<div style="text-align:center;padding:32px 0;color:#8B95A1;font-family:Pretendard,sans-serif"><div style="font-size:36px;margin-bottom:8px">🌙</div><div style="font-size:15px;font-weight:700;color:#4E5968">오늘 롯데 경기 없음</div></div>'
            big_h = 200
        html_card("⚾ 오늘 롯데 자이언츠 경기", big, height=big_h)

        # 문자 중계 (iframe은 별도 컴포넌트라 단일 호출 불가)
        if lotg and lotg[0].get("game_id"):
            live_url = f"https://www.koreabaseball.com/GameCenter/Main.aspx?gameId={lotg[0]['game_id']}"
        else:
            live_url = "https://sports.daum.net/match/80090756"
        st.markdown('<div class="T-card"><div class="T-card-title">📡 실시간 문자 중계 <span class="S-live" style="font-size:11px"><span class="ldot"></span>LIVE</span></div><p style="font-size:13px;color:#8B95A1;margin-bottom:14px">경기 중일 때 실시간 중계를 확인할 수 있습니다</p>', unsafe_allow_html=True)
        st.components.v1.iframe(live_url, height=500, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with gc2:
        # 하이라이트 — 단일 호출
        if hl:
            yt_items = ""
            for v in hl[:3]:
                vid = v["id"]
                thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                yt_items += f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank" style="display:flex;gap:12px;background:#fff;border:1.5px solid #ECEEF2;border-radius:14px;padding:12px;margin-bottom:10px;text-decoration:none"><img src="{thumb}" width="104" height="62" style="object-fit:cover;border-radius:8px;flex-shrink:0"><div><div style="font-size:12px;font-weight:700;color:#191F28;line-height:1.5">{v.get("title","")[:46]}</div><div style="font-size:11px;color:#8B95A1;margin-top:3px">{v.get("channel","")} · {v.get("time","")}</div></div></a>'
            hl_body = yt_items
        else:
            hl_body = '<div style="text-align:center;padding:20px 0;color:#8B95A1;font-family:Pretendard,sans-serif">🎬 영상을 불러오지 못했어요</div>'
        yt_more2 = '<a href="https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D" target="_blank" style="display:block;text-align:center;margin-top:4px;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif">▶ YouTube 더보기</a>'
        html_card("🎬 최신 하이라이트", hl_body + yt_more2, height=460)

        # 티켓 — html_card
        ticket2 = '<p style="font-size:13px;color:#6B7684;margin-bottom:14px;line-height:1.8;font-family:Pretendard,sans-serif">일반 예매 오픈<br>경기 <strong style="color:#3182F6">1주일 전 오후 2시</strong></p><a href="https://ticket.giantsclub.com/loginForm.do" target="_blank" style="display:block;text-align:center;padding:10px;background:#3182F6;color:#fff;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif;margin-bottom:8px">🎫 예매 페이지</a><a href="https://www.giantsclub.com/html/?pcode=257" target="_blank" style="display:block;text-align:center;padding:10px;background:#F2F4F7;color:#333D4B;border-radius:12px;font-weight:700;font-size:14px;font-family:Pretendard,sans-serif">📋 시즌 일정</a>'
        html_card("🎟️ 티켓 예매", ticket2, height=220)


# ════════════════════════════════════════════════════
#  📋 게시판
# ════════════════════════════════════════════════════
with t_board:
    CATS = ["자유","응원","분석","질문","거래"]

    # ── 목록 ──────────────────────────────
    if st.session_state.bv == "list":
        h1, h2 = st.columns([8, 2])
        with h1:
            st.markdown("""
            <p style="font-size:22px;font-weight:900;color:#191F28;margin:0 0 4px;letter-spacing:-.5px">📋 팬 게시판</p>
            <p style="font-size:14px;color:#8B95A1;margin:0 0 20px">롯데 자이언츠 팬들과 이야기를 나눠보세요</p>
            """, unsafe_allow_html=True)
        with h2:
            if st.button("✏️  글쓰기", type="primary", use_container_width=True):
                st.session_state.bv = "write"; st.rerun()

        fc1, _ = st.columns([2, 8])
        with fc1:
            cf = st.selectbox("카테고리", ["전체"]+CATS, label_visibility="collapsed")

        if not sb:
            st.warning("⚠️ Supabase 연결이 필요합니다. `.streamlit/secrets.toml`을 설정하세요.")
        else:
            posts = db_posts(cf)
            if not posts:
                st.markdown('<div class="EMPTY" style="padding:60px 0"><div class="EMPTY-i">📝</div><div class="EMPTY-t">아직 게시글이 없어요</div><div class="EMPTY-s">첫 번째 글을 작성해보세요!</div></div>', unsafe_allow_html=True)
            else:
                for p in posts:
                    cat = p.get("category","자유")
                    c1, c2 = st.columns([13, 1])
                    with c1:
                        st.markdown(f"""
                        <div class="P-row">
                            <span class="P-cat {cat}">{cat}</span>
                            <span class="P-title">{p.get('title','')}</span>
                            <div class="P-meta">
                                <span>✍️ {p.get('author','익명')}</span>
                                <span>👁 {p.get('views',0)}</span>
                                <span>❤️ {p.get('likes',0)}</span>
                                <span>🕐 {fmt_dt(p.get('created_at',''))}</span>
                            </div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        if st.button("→", key=f"r_{p['id']}", use_container_width=True):
                            st.session_state.bv = "detail"
                            st.session_state.pid = p["id"]
                            db_inc_views(p["id"]); st.rerun()

    # ── 글쓰기 ────────────────────────────
    elif st.session_state.bv == "write":
        if st.button("← 목록으로", type="secondary"):
            st.session_state.bv = "list"; st.rerun()

        st.markdown('<div class="T-card" style="max-width:860px"><div class="T-card-title">✏️ 새 게시글 작성</div>', unsafe_allow_html=True)

        wc1, wc2 = st.columns([3, 1])
        with wc1: wt  = st.text_input("제목 *", placeholder="제목을 입력하세요")
        with wc2: wcat= st.selectbox("카테고리", CATS)
        ac1, ac2 = st.columns(2)
        with ac1: wa  = st.text_input("닉네임", placeholder="미입력 시 익명")
        with ac2: wpw = st.text_input("삭제 비밀번호", type="password", placeholder="나중에 삭제할 때 필요")
        wc = st.text_area("내용 *", placeholder="내용을 자유롭게 입력하세요...", height=280)

        b1, b2, _ = st.columns([2, 2, 6])
        with b1:
            if st.button("게시하기 →", type="primary", use_container_width=True):
                if not wt.strip():   st.warning("제목을 입력해주세요.")
                elif not wc.strip(): st.warning("내용을 입력해주세요.")
                elif db_create_post(wt.strip(), wc.strip(), wa.strip(), wpw, wcat):
                    st.success("✅ 게시글이 등록됐습니다!")
                    st.session_state.bv = "list"; st.rerun()
        with b2:
            if st.button("취소", type="secondary", use_container_width=True):
                st.session_state.bv = "list"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 상세 보기 ─────────────────────────
    elif st.session_state.bv == "detail":
        if st.button("← 목록으로", type="secondary"):
            st.session_state.bv = "list"; st.session_state.pid = None; st.rerun()

        post = db_post(st.session_state.pid)
        if not post:
            st.error("게시글을 찾을 수 없습니다.")
        else:
            cat = post.get("category","자유")
            # 게시글 본문
            st.markdown(f"""
            <div class="POST-wrap">
                <span class="P-cat {cat}">{cat}</span>
                <div class="POST-title">{post.get('title','')}</div>
                <div class="POST-meta">
                    <span>✍️ <strong>{post.get('author','익명')}</strong></span>
                    <span>📅 {fmt_dt(post.get('created_at',''),'long')}</span>
                    <span>👁 조회 {post.get('views',0)}</span>
                    <span>❤️ 좋아요 {post.get('likes',0)}</span>
                </div>
                <hr class="DIVIDER">
                <div class="POST-body">{post.get('content','')}</div>
            </div>""", unsafe_allow_html=True)

            # 액션
            a1, a2, _ = st.columns([2, 2, 8])
            with a1:
                if st.button(f"❤️  좋아요  ({post.get('likes',0)})", type="primary", use_container_width=True):
                    db_like(st.session_state.pid); st.rerun()
            with a2:
                with st.expander("🗑️  삭제하기"):
                    dp = st.text_input("삭제 비밀번호", type="password", key="dpw")
                    if st.button("삭제 확인", type="secondary"):
                        ok, msg = db_delete_post(st.session_state.pid, dp)
                        if ok:
                            st.session_state.bv = "list"; st.session_state.pid = None; st.rerun()
                        else: st.error(msg)

            # 댓글
            cmts = db_comments(st.session_state.pid)
            st.markdown(f'<div class="T-card"><div class="T-card-title">💬 댓글 {len(cmts)}개</div>', unsafe_allow_html=True)
            if cmts:
                for c in cmts:
                    st.markdown(f"""
                    <div class="CMT-item">
                        <span class="CMT-author">{c.get('author','익명')}</span>
                        <span class="CMT-time">{fmt_dt(c.get('created_at',''))}</span>
                        <div class="CMT-body">{c.get('content','')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<p style="text-align:center;color:#8B95A1;font-size:14px;padding:16px 0">첫 댓글을 남겨보세요! 💬</p>', unsafe_allow_html=True)

            st.markdown('<hr class="DIVIDER">', unsafe_allow_html=True)
            cc1, cc2 = st.columns([1, 3])
            with cc1: ca = st.text_input("닉네임", placeholder="익명", key="ca")
            with cc2: cc_val = st.text_input("댓글 내용을 입력하세요", key="cc")
            if st.button("댓글 등록", type="primary"):
                if cc_val.strip():
                    db_add_comment(st.session_state.pid, ca.strip(), cc_val.strip()); st.rerun()
                else: st.warning("댓글 내용을 입력해주세요.")
            st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  🎯 승부예측
# ════════════════════════════════════════════════════
with t_predict:
    # ── 데이터 준비
    pred_games    = get_today_games()
    pred_standing = get_standings()
    pred_votes    = db_today_votes()

    # 오늘 롯데 경기 찾기
    lotte_game = next((g for g in pred_games if g["is_lotte"]), None)

    # 상대팀 이름
    if lotte_game:
        opp_name = lotte_game["home"] if lotte_game["away"] == "롯데" else lotte_game["away"]
        lotte_is_home = lotte_game["home"] == "롯데"
        game_state = lotte_game["state"]
        game_score = lotte_game["score"]
        stad_name  = lotte_game.get("stadium","")
    else:
        opp_name = "상대팀"
        lotte_is_home = True
        game_state = ""
        game_score = "vs"
        stad_name = ""

    # 승률 기반 예측 확률 계산
    def get_win_rate(team_name, df):
        if df is None: return 0.5
        row = df[df["팀"].str.contains(team_name, na=False)]
        if row.empty: return 0.5
        try: return float(str(row.iloc[0].get("승률","0.500")).replace(",",""))
        except: return 0.5

    lotte_wr = get_win_rate("롯데", pred_standing)
    opp_wr   = get_win_rate(opp_name, pred_standing) if opp_name != "상대팀" else 0.5

    total_wr = lotte_wr + opp_wr
    if total_wr > 0:
        ai_lotte_pct = round(lotte_wr / total_wr * 100, 1)
    else:
        ai_lotte_pct = 50.0
    ai_opp_pct = round(100 - ai_lotte_pct, 1)

    # 순위 가져오기
    def get_rank(team_name, df):
        if df is None: return "-"
        row = df[df["팀"].str.contains(team_name, na=False)]
        return str(row.iloc[0].get("순위","-")) if not row.empty else "-"

    lotte_rank = get_rank("롯데", pred_standing)
    opp_rank   = get_rank(opp_name, pred_standing) if opp_name != "상대팀" else "-"
    lotte_logo = TEAM_LOGO.get("롯데","")
    opp_logo   = TEAM_LOGO.get(opp_name,"")

    # 투표 집계
    tv = len(pred_votes)
    vote_ln = len(pred_votes[pred_votes["selected_team"]=="롯데"]) if tv > 0 else 0
    vote_on = tv - vote_ln
    vote_lp = round(vote_ln/tv*100, 1) if tv > 0 else 50.0
    vote_op = round(100 - vote_lp, 1)

    # ── 레이아웃
    pr1, pr2 = st.columns([5, 7], gap="medium")

    with pr1:
        # ── 오늘 경기 매치업 카드
        bdg_html = state_badge_inline(game_state, lotte_game["time"] if lotte_game else "")
        l_img = f'<img src="{lotte_logo}" width="64" height="64" style="object-fit:contain">' if lotte_logo else '<div style="width:64px;height:64px;background:#FEF2F2;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:#DC2626">롯데</div>'
        o_img = f'<img src="{opp_logo}" width="64" height="64" style="object-fit:contain">' if opp_logo else f'<div style="width:64px;height:64px;background:#EFF6FF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#1D4ED8">{opp_name}</div>'

        matchup_body = f"""
<div style="text-align:center;padding:24px 0 20px">
  <div style="margin-bottom:12px">{bdg_html}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:20px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex:1">
      {l_img}
      <div style="font-size:17px;font-weight:900;color:#191F28">롯데</div>
      <div style="font-size:11px;color:#8B95A1;font-weight:600">{'홈' if lotte_is_home else '원정'} · {lotte_rank}위</div>
      <div style="font-size:12px;color:#8B95A1">시즌 승률 {lotte_wr:.3f}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:48px">
      <div style="font-size:13px;color:#D1D5DB;font-weight:400">vs</div>
      {"<div style='font-size:11px;color:#9CA3AF;font-weight:600'>🏟 "+stad_name+"</div>" if stad_name else ""}
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;flex:1">
      {o_img}
      <div style="font-size:17px;font-weight:900;color:#191F28">{opp_name}</div>
      <div style="font-size:11px;color:#8B95A1;font-weight:600">{'원정' if lotte_is_home else '홈'} · {opp_rank}위</div>
      <div style="font-size:12px;color:#8B95A1">시즌 승률 {opp_wr:.3f}</div>
    </div>
  </div>
</div>"""
        html_card(f"⚾ {today.strftime('%m월 %d일')} 오늘의 경기", matchup_body, height=280 if lotte_game else 180)

        # ── AI 예측 확률 카드
        ai_color  = "#DC2626" if ai_lotte_pct >= 50 else "#1D4ED8"
        ai_winner = "롯데 자이언츠" if ai_lotte_pct >= 50 else opp_name
        ai_emoji  = "🔴" if ai_lotte_pct >= 50 else "💙"
        tip_msgs = []
        if pred_standing is not None:
            l_row = pred_standing[pred_standing["팀"].str.contains("롯데",na=False)]
            o_row = pred_standing[pred_standing["팀"].str.contains(opp_name,na=False)] if opp_name != "상대팀" else pd.DataFrame()
            if not l_row.empty and not o_row.empty:
                lr, orr = int(l_row.iloc[0].get("순위",10)), int(o_row.iloc[0].get("순위",10))
                if lr < orr: tip_msgs.append(f"롯데가 {opp_name}보다 {orr-lr}계단 높은 순위")
                elif lr > orr: tip_msgs.append(f"{opp_name}이(가) 롯데보다 {lr-orr}계단 높은 순위")
        tip_html = f'<div style="font-size:12px;color:#6B7684;margin-top:8px">📊 {" · ".join(tip_msgs)}</div>' if tip_msgs else ""

        ai_body = f"""
<div style="text-align:center;padding:8px 0 4px">
  <div style="font-size:13px;color:#8B95A1;font-weight:600;margin-bottom:16px">순위표 승률 기반 AI 예측</div>
  <div style="display:flex;align-items:flex-end;justify-content:center;gap:16px;margin-bottom:16px">
    <div style="text-align:center">
      <div style="font-size:42px;font-weight:900;color:#DC2626;line-height:1">{ai_lotte_pct}%</div>
      <div style="font-size:12px;color:#DC2626;font-weight:700;margin-top:4px">🔴 롯데</div>
    </div>
    <div style="font-size:22px;color:#E5E7EB;font-weight:300;padding-bottom:12px">:</div>
    <div style="text-align:center">
      <div style="font-size:42px;font-weight:900;color:#1D4ED8;line-height:1">{ai_opp_pct}%</div>
      <div style="font-size:12px;color:#1D4ED8;font-weight:700;margin-top:4px">💙 {opp_name}</div>
    </div>
  </div>
  <div style="height:10px;border-radius:999px;overflow:hidden;background:#F2F4F7;margin-bottom:14px">
    <div style="height:100%;width:{ai_lotte_pct}%;background:linear-gradient(90deg,#991B1B,#EF4444);border-radius:999px"></div>
  </div>
  <div style="background:{'#FEF2F2' if ai_lotte_pct>=50 else '#EFF6FF'};border-radius:12px;padding:12px 16px;display:inline-block">
    <span style="font-size:14px;font-weight:800;color:{ai_color}">{ai_emoji} {ai_winner} 승리 예측</span>
  </div>
  {tip_html}
</div>"""
        html_card("🤖 AI 승리 예측", ai_body, height=280)

        # ── 투표 입력 카드
        if not sb:
            st.warning("⚠️ 데이터베이스 연결이 필요합니다.")
        else:
            with st.container(border=True):
                st.markdown('<p style="font-size:17px;font-weight:800;color:#191F28;margin:0 0 16px;letter-spacing:-.3px">🗳️ 당신의 승부 예측은?</p>', unsafe_allow_html=True)
                pn = st.text_input("닉네임", placeholder="닉네임을 입력하세요", key="pn")
                pt = st.radio(
                    "팀 선택",
                    [f"🔴 롯데 자이언츠 이겨라!!", f"💙 {opp_name} 이길 것 같아요"],
                    label_visibility="collapsed"
                )
                if st.button("🎯  예측 제출하기", type="primary", use_container_width=True):
                    if not pn.strip():
                        st.warning("닉네임을 입력해주세요.")
                    elif tv > 0 and pn.strip() in pred_votes["nickname"].values:
                        st.warning("이미 오늘 예측을 완료했어요! 😊")
                    else:
                        team_val = "롯데" if "롯데" in pt else "상대팀"
                        if db_add_vote(pn.strip(), team_val):
                            st.success(f"✅ {pn.strip()}님의 예측이 등록됐어요!")
                            st.balloons(); st.rerun()
                        else:
                            st.error("등록에 실패했습니다.")

    with pr2:
        # ── 팬 투표 현황 카드
        lv_names = pred_votes[pred_votes["selected_team"]=="롯데"]["nickname"].tolist() if tv > 0 else []
        ov_names = pred_votes[pred_votes["selected_team"]=="상대팀"]["nickname"].tolist() if tv > 0 else []

        lotte_tags = "".join([f'<span style="display:inline-flex;align-items:center;background:#FEF2F2;color:#DC2626;border-radius:8px;padding:5px 11px;font-size:12px;font-weight:700;margin:3px">⚾ {n}</span>' for n in lv_names])
        opp_tags   = "".join([f'<span style="display:inline-flex;align-items:center;background:#EFF6FF;color:#1D4ED8;border-radius:8px;padding:5px 11px;font-size:12px;font-weight:700;margin:3px">💙 {n}</span>' for n in ov_names])

        if tv > 0:
            vote_bar = f"""
<div style="display:flex;justify-content:space-between;margin-bottom:8px">
  <span style="font-size:16px;font-weight:900;color:#DC2626">🔴 롯데 {vote_lp}%</span>
  <span style="font-size:16px;font-weight:900;color:#1D4ED8">{vote_op}% {opp_name} 💙</span>
</div>
<div style="display:flex;height:60px;border-radius:16px;overflow:hidden;background:#F2F4F7;margin-bottom:20px">
  <div style="width:{vote_lp}%;background:linear-gradient(90deg,#991B1B,#EF4444);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:15px">{"롯데" if vote_lp>18 else ""}</div>
  <div style="flex:1;background:linear-gradient(90deg,#1E40AF,#3B82F6);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:15px">{opp_name if vote_op>18 else ""}</div>
</div>
<div style="text-align:center;font-size:12px;color:#8B95A1;font-weight:600;margin-bottom:20px">총 {tv}명 참여</div>"""

            col_v = "#DC2626" if vote_lp>60 else "#1D4ED8" if vote_lp<40 else "#D97706"
            msg_v = (f"팬들의 {vote_lp}%가 롯데 승리를 예측해요! 💪" if vote_lp>60
                     else f"팬들의 {vote_op}%가 {opp_name} 승리를 예측해요 🔥" if vote_lp<40
                     else "팬들도 반반! 박빙의 명승부 예상 ⚡")
            fan_comment = f'<div style="background:#F8F9FA;border-radius:12px;padding:14px 16px;margin-bottom:20px;border-left:4px solid {col_v}"><span style="font-size:14px;color:#333D4B;font-weight:700">{msg_v}</span></div>'

            voter_section = ""
            if lv_names:
                voter_section += f'<div style="margin-bottom:14px"><div style="font-size:13px;font-weight:800;color:#DC2626;margin-bottom:8px">🔴 롯데 응원단 ({len(lv_names)}명)</div><div>{lotte_tags}</div></div>'
            if ov_names:
                voter_section += f'<div><div style="font-size:13px;font-weight:800;color:#1D4ED8;margin-bottom:8px">💙 {opp_name} 응원단 ({len(ov_names)}명)</div><div>{opp_tags}</div></div>'

            vote_content = vote_bar + fan_comment + voter_section
        else:
            vote_content = '<div style="text-align:center;padding:52px 0;color:#8B95A1"><div style="font-size:44px;margin-bottom:12px">🗳️</div><div style="font-size:16px;font-weight:700;color:#4E5968;margin-bottom:6px">아직 예측이 없어요</div><div style="font-size:13px">왼쪽에서 첫 번째 예측자가 되어보세요!</div></div>'

        html_card("📊 팬 투표 현황", vote_content, height=600)

        # ── 참여 통계 카드
        stat_body = f"""
<div style="display:flex;gap:12px">
  <div style="flex:1;background:#F8F9FA;border-radius:14px;padding:18px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:#191F28;line-height:1">{tv}</div>
    <div style="font-size:12px;color:#8B95A1;font-weight:600;margin-top:6px">총 참여</div>
  </div>
  <div style="flex:1;background:#FEF2F2;border-radius:14px;padding:18px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:#DC2626;line-height:1">{vote_ln}</div>
    <div style="font-size:12px;color:#DC2626;font-weight:600;margin-top:6px">롯데 응원</div>
  </div>
  <div style="flex:1;background:#EFF6FF;border-radius:14px;padding:18px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:#1D4ED8;line-height:1">{vote_on}</div>
    <div style="font-size:12px;color:#1D4ED8;font-weight:600;margin-top:6px">{opp_name} 응원</div>
  </div>
</div>"""
        html_card("📈 오늘 참여 통계", stat_body, height=180)


# ── 푸터
st.markdown(f'<div style="text-align:center;padding:40px 0 20px;color:#B0B8C1;font-size:13px;font-weight:500;line-height:1.8">⚾ 부산갈매기 · 롯데 자이언츠 비공식 팬 플랫폼<br><span style="font-size:12px;color:#D1D5DB">데이터: KBO 공식, 네이버 스포츠, Google News, YouTube</span></div>', unsafe_allow_html=True)
