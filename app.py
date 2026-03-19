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

/* ── 애니메이션 ── */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }
.ldot {
    display: inline-block; width: 7px; height: 7px;
    border-radius: 50%; background: #EF4444;
    animation: blink 1.4s infinite;
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
.T-table { width: 100%; border-collapse: collapse; }
.T-table th {
    background: #F8F9FB; color: #8B95A1 !important; font-weight: 700;
    padding: 10px 6px; text-align: center; font-size: 11px;
    letter-spacing: .4px; border-bottom: 2px solid #ECEEF2; text-transform: uppercase;
}
.T-table td {
    padding: 12px 6px; text-align: center;
    color: #333D4B !important; border-bottom: 1px solid #F5F6F8; font-size: 13px;
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
.YT-thumb { width:108px;height:66px;object-fit:cover;border-radius:8px;flex-shrink:0; }
.YT-ttl { font-size:13px !important;font-weight:700 !important;color:#191F28 !important;line-height:1.5;margin-bottom:4px; }
.YT-meta { font-size:11px !important;color:#8B95A1 !important; }

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


@st.cache_data(ttl=90)
def get_today_games():
    """
    KBO 오늘 경기 파싱
    - 시범경기(srId=0) / 정규시즌(srId=1) 자동 감지
    - 소스 1: KBO 공식 GetScheduleList API
    - 소스 2: 네이버 스포츠 일정 API
    - 소스 3: HTML fallback
    """
    KT = {
        "LT":"롯데","SS":"삼성","LG":"LG","OB":"두산",
        "KT":"KT","SK":"SSG","HH":"한화","NC":"NC","HT":"KIA","WO":"키움",
    }
    today_str = today.strftime("%Y%m%d")
    games = []

    # ── 소스 1: KBO 공식 API (시범경기 srId=0 포함)
    for sr_id in ["0", "1", "0,1,3,4,5,7,8,9"]:
        if games:
            break
        for endpoint in [
            "https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList",
            "https://www.koreabaseball.com/ws/Main.asmx/GetKBOGameList",
        ]:
            try:
                payload = {"leId": "1", "srId": sr_id, "date": today_str}
                res = requests.post(
                    endpoint, data=payload,
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
                # 여러 키 시도
                glist = (data.get("game") or data.get("data") or
                         data.get("games") or data.get("result") or [])
                for g in glist:
                    away_cd = g.get("visitTeamCode", g.get("awayTeamCode",""))
                    home_cd = g.get("homeTeamCode","")
                    away = KT.get(away_cd, g.get("visitTeamName", g.get("awayTeamName", away_cd)))
                    home = KT.get(home_cd, g.get("homeTeamName", home_cd))
                    vs = str(g.get("visitScore", g.get("awayScore","")))
                    hs = str(g.get("homeScore",""))
                    score = f"{vs}:{hs}" if vs not in ("","None","-") and hs not in ("","None","-") else "vs"
                    sc = str(g.get("status", g.get("statusCode", g.get("gameStatus",""))))
                    state = ("종료" if sc in ("3","경기종료","RESULT","종료") else
                             "진행중" if sc in ("1","경기중","LIVE","진행중") else
                             "취소" if "취소" in sc else "")
                    gt = g.get("gameTime", g.get("gtime", g.get("startTime",""))) or ""
                    time_s = gt[:5] if gt else ""
                    stad = g.get("stadiumName", g.get("stadium", g.get("venueName","")))
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

    # ── 소스 2: 네이버 스포츠 API (시범경기 roundCode=1)
    if not games:
        for round_code in ["1", "0", "2"]:
            try:
                url = (f"https://api-gw.sports.naver.com/schedule/games"
                       f"?fields=basic&upperCategoryId=kbaseball&categoryId=kbo"
                       f"&date={today_str}&roundCode={round_code}&size=20")
                nv_hdr = {**HDR, "Referer": "https://sports.news.naver.com/",
                          "Origin": "https://sports.news.naver.com"}
                res = requests.get(url, headers=nv_hdr, timeout=10)
                if res.status_code != 200:
                    continue
                data = res.json()
                glist = data.get("games", data.get("game", data.get("result", [])))
                for g in glist:
                    away = g.get("awayTeamName", g.get("visitTeamName",""))
                    home = g.get("homeTeamName","")
                    vs   = g.get("awayScore", g.get("visitScore",""))
                    hs   = g.get("homeScore","")
                    score = f"{vs}:{hs}" if str(vs) not in ("","None") and str(hs) not in ("","None") else "vs"
                    sc    = g.get("statusCode", g.get("status",""))
                    state = ("진행중" if sc in ("LIVE","1") else
                             "종료"   if sc in ("RESULT","3") else
                             "취소"   if "CANCEL" in str(sc) else "")
                    gt    = g.get("startTime", g.get("gameTime","")) or ""
                    time_s = gt[:5] if gt else ""
                    stad   = g.get("venueName", g.get("stadiumName",""))
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

    # ── 소스 3: 네이버 스포츠 HTML 파싱 (최후 수단)
    if not games:
        try:
            url = f"https://sports.news.naver.com/kbaseball/schedule/index?date={today_str}"
            res = requests.get(url, headers={**HDR, "Referer": "https://sports.news.naver.com/"}, timeout=12)
            soup = BeautifulSoup(res.text, "html.parser")
            kbo_teams = ["롯데","삼성","LG","두산","KT","SSG","한화","NC","KIA","키움"]
            stadiums   = ["사직","잠실","수원","대전","고척","창원","광주","대구","인천","포항","청주"]
            seen = set()
            for row in soup.select("tr, li"):
                text = row.get_text(" ", strip=True)
                found = [t for t in kbo_teams if t in text]
                if len(found) < 2:
                    continue
                key = f"{found[0]}{found[1]}"
                if key in seen:
                    continue
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
def state_badge(state, time_s):
    if state == "진행중":
        return f'<span class="S-live"><span class="ldot"></span>진행중</span>'
    elif state == "종료":
        return '<span class="S-done">종료</span>'
    elif state == "취소":
        return '<span class="S-cancel">취소</span>'
    else:
        return f'<span class="S-sched">{"⏰ "+time_s if time_s else "예정"}</span>'


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

    cL, cC, cR = st.columns([1.4, 2.8, 1.5], gap="medium")

    # ─ 왼쪽
    with cL:
        # KBO 순위
        st.markdown('<div class="T-card"><div class="T-card-title">🏆 KBO 리그 순위</div>', unsafe_allow_html=True)
        if standings is not None:
            rows = ""
            for _, r in standings.iterrows():
                rank = str(r.get("순위",""))
                is_l = "롯데" in str(r.get("팀",""))
                rc = {"1":"RN1","2":"RN2","3":"RN3"}.get(rank,"RNn")
                rows += f"""<tr class="{'HL' if is_l else ''}">
                    <td><span class="RN {rc}">{rank}</span></td>
                    <td style="text-align:left;padding-left:8px;font-weight:{'900' if is_l else '500'};color:{'#1D4ED8' if is_l else '#333D4B'}">
                        {r.get('팀','')}
                    </td>
                    <td style="color:{'#1D4ED8' if is_l else '#333D4B'}">{r.get('승','')}</td>
                    <td style="color:{'#1D4ED8' if is_l else '#6B7684'}">{r.get('패','')}</td>
                    <td style="color:{'#1D4ED8' if is_l else '#333D4B'}">{r.get('승률','')}</td>
                    <td style="color:#8B95A1">{r.get('게임차','')}</td>
                </tr>"""
            st.markdown(f"""
            <table class="T-table">
                <thead><tr>
                    <th>순위</th><th style="text-align:left;padding-left:8px">팀</th>
                    <th>승</th><th>패</th><th>승률</th><th>게임차</th>
                </tr></thead>
                <tbody>{rows}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY"><div class="EMPTY-i">📡</div><div class="EMPTY-t">순위 로딩 실패</div><div class="EMPTY-s">새로고침 해주세요</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 예측 미리보기
        tv = len(votes)
        st.markdown('<div class="T-card"><div class="T-card-title">🎯 오늘의 예측 현황</div>', unsafe_allow_html=True)
        if tv > 0:
            ln = len(votes[votes["selected_team"]=="롯데"])
            lp = round(ln/tv*100,1); op = round(100-lp,1)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:800;margin-bottom:8px;color:#191F28">
                <span style="color:#DC2626">🔴 롯데 {lp}%</span>
                <span style="color:#1D4ED8">{op}% 상대팀 💙</span>
            </div>
            <div class="VB-wrap">
                <div class="VB-l" style="width:{lp}%">{"롯데" if lp>20 else ""}</div>
                <div class="VB-r">{"상대팀" if op>20 else ""}</div>
            </div>
            <p style="text-align:center;font-size:12px;color:#8B95A1;margin-top:8px;font-weight:600">총 {tv}명 참여 중</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:18px 0"><div class="EMPTY-i">🗳️</div><div class="EMPTY-t">아직 예측이 없어요</div><div class="EMPTY-s">승부예측 탭에서 투표하세요!</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─ 가운데
    with cC:
        # 오늘 경기
        st.markdown(f'<div class="T-card"><div class="T-card-title">📅 오늘의 KBO 경기 <span style="font-size:13px;color:#8B95A1;font-weight:500">· {today.strftime("%m/%d")}</span></div>', unsafe_allow_html=True)
        if today_games:
            for g in today_games:
                aw, hm = g["away"], g["home"]
                is_l = g["is_lotte"]
                bdg  = state_badge(g["state"], g["time"])
                st.markdown(f"""
                <div class="G-card {'lotte' if is_l else ''}">
                    <div style="display:flex;align-items:center;justify-content:center;gap:20px;flex:1">
                        <span class="G-team" style="min-width:56px;text-align:right">{aw}</span>
                        <div style="text-align:center">
                            <div class="G-score">{g['score']}</div>
                            <div style="margin-top:7px;display:flex;gap:6px;justify-content:center;align-items:center">
                                {bdg}
                                <span class="G-meta">{'🏟 '+g['stadium'] if g['stadium'] else ''}</span>
                            </div>
                        </div>
                        <span class="G-team" style="min-width:56px">{hm}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:28px 0"><div class="EMPTY-i">🌙</div><div class="EMPTY-t">경기 정보를 불러오지 못했어요</div><div class="EMPTY-s">아래 버튼에서 직접 확인하세요</div></div>', unsafe_allow_html=True)
            with st.expander("🔧 파싱 디버그 (개발용)"):
                today_str = today.strftime("%Y%m%d")
                st.write(f"조회 날짜: {today_str}")
                for sr in ["0","1"]:
                    try:
                        r = requests.post(
                            "https://www.koreabaseball.com/ws/Schedule.asmx/GetScheduleList",
                            data={"leId":"1","srId":sr,"date":today_str},
                            headers={**HDR,"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","X-Requested-With":"XMLHttpRequest"},
                            timeout=8)
                        st.write(f"KBO API (srId={sr}) → status:{r.status_code}")
                        if r.status_code == 200:
                            st.code(r.text[:500])
                    except Exception as e:
                        st.write(f"KBO API (srId={sr}) → 오류: {e}")
                try:
                    r2 = requests.get(
                        f"https://api-gw.sports.naver.com/schedule/games?fields=basic&upperCategoryId=kbaseball&categoryId=kbo&date={today_str}&roundCode=1&size=20",
                        headers={**HDR,"Referer":"https://sports.news.naver.com/"}, timeout=8)
                    st.write(f"Naver API → status:{r2.status_code}")
                    if r2.status_code == 200:
                        st.code(r2.text[:500])
                except Exception as e:
                    st.write(f"Naver API → 오류: {e}")
        st.link_button(f"📋 네이버 스포츠 오늘 경기", f"https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime('%Y%m%d')}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 뉴스
        st.markdown('<div class="T-card"><div class="T-card-title">📰 롯데 자이언츠 최신 뉴스</div>', unsafe_allow_html=True)
        if news_list:
            for i, n in enumerate(news_list[:8], 1):
                st.markdown(f"""
                <div class="N-item">
                    <span class="N-num">{i}</span>
                    <div>
                        <div class="N-title"><a href="{n['url']}" target="_blank">{n['title']}</a></div>
                        <div class="N-press">{n.get('press','')} · {n.get('pub','')}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:20px 0"><div class="EMPTY-i">📡</div><div class="EMPTY-t">뉴스를 불러오지 못했어요</div></div>', unsafe_allow_html=True)
        st.link_button("🔗 네이버 스포츠 뉴스 더보기", "https://sports.news.naver.com/kbaseball/news/index?type=team&teamCode=LT", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ─ 오른쪽
    with cR:
        st.markdown('<div class="T-card"><div class="T-card-title">🎬 최신 하이라이트</div>', unsafe_allow_html=True)
        if highlights:
            for v in highlights[:2]:
                vid = v["id"]
                thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                st.markdown(f"""
                <a class="YT-card" href="https://www.youtube.com/watch?v={vid}" target="_blank">
                    <img class="YT-thumb" src="{thumb}" onerror="this.src='https://img.youtube.com/vi/{vid}/hqdefault.jpg'" alt="">
                    <div>
                        <div class="YT-ttl">{v.get('title','')[:52]}</div>
                        <div class="YT-meta">{v.get('channel','')} · {v.get('time','')}</div>
                    </div>
                </a>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:20px 0"><div class="EMPTY-i">🎬</div><div class="EMPTY-t">영상 로딩 실패</div></div>', unsafe_allow_html=True)
        st.link_button("▶ YouTube 더보기", "https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="T-card"><div class="T-card-title">🎟️ 티켓 예매</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#6B7684;margin-bottom:14px;line-height:1.8">일반 예매 오픈<br>경기 <strong style="color:#3182F6">1주일 전 오후 2시</strong></p>', unsafe_allow_html=True)
        st.link_button("🎫 예매 페이지", "https://ticket.giantsclub.com/loginForm.do", use_container_width=True)
        st.link_button("📋 시즌 일정", "https://www.giantsclub.com/html/?pcode=257", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  ⚾ 경기
# ════════════════════════════════════════════════════
with t_game:
    tg   = get_today_games()
    hl   = get_youtube_highlights()
    lotg = [g for g in tg if g["is_lotte"]]

    gc1, gc2 = st.columns([3, 2], gap="medium")

    with gc1:
        # 롯데 오늘 경기 빅 카드
        st.markdown('<div class="T-card"><div class="T-card-title">⚾ 오늘 롯데 자이언츠 경기</div>', unsafe_allow_html=True)
        if lotg:
            g = lotg[0]
            aw, hm = g["away"], g["home"]
            bdg = state_badge(g["state"], g["time"])
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:18px;padding:32px;text-align:center">
                <div style="margin-bottom:14px">{bdg}</div>
                <div style="display:flex;align-items:center;justify-content:center;gap:28px">
                    <div>
                        <div style="font-size:26px;font-weight:900;color:#191F28">{aw}</div>
                        <div style="font-size:12px;color:#6B7684;margin-top:4px;font-weight:600">원정</div>
                    </div>
                    <div style="font-size:38px;font-weight:900;color:#191F28;letter-spacing:7px;
                                padding:14px 28px;background:#fff;border-radius:16px;
                                box-shadow:0 4px 16px rgba(0,0,0,.08)">{g['score']}</div>
                    <div>
                        <div style="font-size:26px;font-weight:900;color:#191F28">{hm}</div>
                        <div style="font-size:12px;color:#6B7684;margin-top:4px;font-weight:600">홈</div>
                    </div>
                </div>
                <div style="margin-top:16px;font-size:13px;color:#6B7684;font-weight:600">
                    {'🏟 '+g['stadium'] if g['stadium'] else ''}
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:32px 0"><div class="EMPTY-i">🌙</div><div class="EMPTY-t">오늘 롯데 경기 정보 없음</div><div class="EMPTY-s">아래 버튼에서 확인해보세요</div></div>', unsafe_allow_html=True)
        st.link_button("📋 네이버 스포츠 오늘 경기", f"https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime('%Y%m%d')}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 문자 중계
        st.markdown('<div class="T-card"><div class="T-card-title">📡 실시간 문자 중계 <span class="S-live" style="font-size:11px"><span class="ldot"></span>LIVE</span></div><p style="font-size:13px;color:#8B95A1;margin-bottom:14px">경기 중일 때 실시간 중계를 확인할 수 있습니다</p>', unsafe_allow_html=True)
        st.components.v1.iframe("https://sports.daum.net/match/80090756", height=500, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with gc2:
        # 전체 경기
        st.markdown('<div class="T-card"><div class="T-card-title">📋 오늘 전체 경기</div>', unsafe_allow_html=True)
        if tg:
            for g in tg:
                aw, hm = g["away"], g["home"]
                is_l = g["is_lotte"]
                st.markdown(f"""
                <div class="G-card {'lotte' if is_l else ''}" style="padding:13px 16px">
                    <div style="flex:1;display:flex;align-items:center;justify-content:space-between;gap:8px">
                        <span style="font-size:14px;font-weight:{'900' if is_l else '600'};color:#191F28;min-width:40px;text-align:right">{aw}</span>
                        <span style="background:#F2F4F7;border-radius:8px;padding:5px 14px;font-size:16px;font-weight:900;color:#191F28;letter-spacing:4px">{g['score']}</span>
                        <span style="font-size:14px;font-weight:{'900' if is_l else '600'};color:#191F28;min-width:40px">{hm}</span>
                        {state_badge(g['state'],g['time'])}
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:24px 0"><div class="EMPTY-i">📅</div><div class="EMPTY-t">오늘은 경기가 없어요</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 하이라이트
        st.markdown('<div class="T-card"><div class="T-card-title">🎬 최신 하이라이트</div>', unsafe_allow_html=True)
        if hl:
            for v in hl[:3]:
                vid = v["id"]
                thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                st.markdown(f"""
                <a class="YT-card" href="https://www.youtube.com/watch?v={vid}" target="_blank">
                    <img class="YT-thumb" src="{thumb}" style="width:104px;height:62px" onerror="this.src='https://img.youtube.com/vi/{vid}/hqdefault.jpg'" alt="">
                    <div>
                        <div class="YT-ttl">{v.get('title','')[:46]}</div>
                        <div class="YT-meta">{v.get('channel','')} · {v.get('time','')}</div>
                    </div>
                </a>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:20px 0"><div class="EMPTY-i">🎬</div><div class="EMPTY-t">영상을 불러오지 못했어요</div></div>', unsafe_allow_html=True)
        st.link_button("▶ YouTube 더보기", "https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


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
    votes = db_today_votes()
    tp = len(votes)
    ln = len(votes[votes["selected_team"]=="롯데"]) if tp > 0 else 0
    on = tp - ln
    lp = round(ln/tp*100, 1) if tp > 0 else 50.0
    op = round(100-lp, 1)

    pc1, pc2 = st.columns([5, 7], gap="medium")

    with pc1:
        st.markdown(f"""
        <div class="T-card">
            <div class="T-card-title">🎯 {today.strftime('%m월 %d일')} 승부 예측</div>
            <div style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:16px;
                        padding:22px;text-align:center;margin-bottom:20px">
                <div style="font-size:28px;margin-bottom:8px;font-weight:800;color:#191F28">
                    🔴 롯데 <span style="color:#93C5FD;font-size:20px;font-weight:500">vs</span> 상대팀 💙
                </div>
                <div style="font-size:13px;color:#4E5968;font-weight:600">오늘 경기 승자를 예측해보세요!</div>
            </div>
        """, unsafe_allow_html=True)

        if not sb:
            st.warning("⚠️ 데이터베이스 연결이 필요합니다.")
        else:
            pn = st.text_input("닉네임 *", placeholder="닉네임을 입력하세요", key="pn")
            pt = st.radio(
                "오늘 경기 예측",
                ["🔴 최강 롯데 자이언츠 이겨라!!", "💙 오늘은 상대팀이 이길 것 같아요"],
                label_visibility="visible"
            )
            if st.button("🎯  예측 제출하기", type="primary", use_container_width=True):
                if not pn.strip():
                    st.warning("닉네임을 입력해주세요.")
                elif tp > 0 and pn.strip() in votes["nickname"].values:
                    st.warning("이미 오늘 예측을 완료했어요! 😊")
                else:
                    tv = "롯데" if "롯데" in pt else "상대팀"
                    if db_add_vote(pn.strip(), tv):
                        st.success(f"✅ {pn.strip()}님의 예측이 등록됐어요!")
                        st.balloons(); st.rerun()
                    else:
                        st.error("등록에 실패했습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

        # 통계
        st.markdown('<div class="T-card"><div class="T-card-title">📊 오늘 참여 통계</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f'<div class="ST-box"><div class="ST-val">{tp}</div><div class="ST-lbl">총 참여</div></div>', unsafe_allow_html=True)
        with s2: st.markdown(f'<div class="ST-box"><div class="ST-val" style="color:#DC2626">{ln}</div><div class="ST-lbl">롯데 응원</div></div>', unsafe_allow_html=True)
        with s3: st.markdown(f'<div class="ST-box"><div class="ST-val" style="color:#1D4ED8">{on}</div><div class="ST-lbl">상대팀 응원</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pc2:
        st.markdown('<div class="T-card"><div class="T-card-title">📊 실시간 예측 결과</div>', unsafe_allow_html=True)
        if tp > 0:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                <span style="font-size:17px;font-weight:900;color:#DC2626">🔴 롯데 {lp}%</span>
                <span style="font-size:17px;font-weight:900;color:#1D4ED8">{op}% 상대팀 💙</span>
            </div>
            <div class="VB-wrap" style="height:64px;margin-bottom:24px;border-radius:16px">
                <div class="VB-l" style="width:{lp}%;font-size:17px">{"롯데" if lp>18 else ""}</div>
                <div class="VB-r" style="font-size:17px">{"상대팀" if op>18 else ""}</div>
            </div>""", unsafe_allow_html=True)

            lv = votes[votes["selected_team"]=="롯데"]["nickname"].tolist()
            ov = votes[votes["selected_team"]=="상대팀"]["nickname"].tolist()
            if lv:
                tags = "".join([f'<span class="VTAG">⚾ {n}</span>' for n in lv])
                st.markdown(f'<p style="font-size:14px;font-weight:800;color:#DC2626;margin-bottom:8px">🔴 롯데 응원단 ({len(lv)}명)</p><div style="margin-bottom:18px">{tags}</div>', unsafe_allow_html=True)
            if ov:
                tags = "".join([f'<span class="VTAG">💙 {n}</span>' for n in ov])
                st.markdown(f'<p style="font-size:14px;font-weight:800;color:#1D4ED8;margin-bottom:8px">💙 상대팀 응원단 ({len(ov)}명)</p><div>{tags}</div>', unsafe_allow_html=True)

            col = "#DC2626" if lp>60 else "#1D4ED8" if lp<40 else "#D97706"
            msg = (f"팬들의 {lp}%가 롯데를 응원해요! 오늘도 이겨라!! 💪" if lp>60
                   else f"팬들의 {op}%가 상대팀 응원. 역전의 명수 롯데 파이팅! ⚡" if lp<40
                   else "팽팽한 예측! 명승부가 기대됩니다 🔥")
            st.markdown(f'<div style="background:#F8F9FA;border-radius:14px;padding:16px 20px;margin-top:20px;border-left:4px solid {col}"><p style="font-size:14px;color:#333D4B;margin:0;font-weight:700;line-height:1.6">{msg}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="EMPTY" style="padding:64px 0"><div class="EMPTY-i">🎯</div><div class="EMPTY-t">아직 예측이 없어요</div><div class="EMPTY-s">왼쪽에서 첫 번째 예측자가 되어보세요! 👈</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── 푸터
st.markdown(f'<div style="text-align:center;padding:40px 0 20px;color:#B0B8C1;font-size:13px;font-weight:500;line-height:1.8">⚾ 부산갈매기 · 롯데 자이언츠 비공식 팬 플랫폼<br><span style="font-size:12px;color:#D1D5DB">데이터: KBO 공식, 네이버 스포츠, Google News, YouTube</span></div>', unsafe_allow_html=True)
