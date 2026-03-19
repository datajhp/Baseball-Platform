"""
부산갈매기 ⚾ 롯데 자이언츠 팬 플랫폼
"""
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from datetime import datetime as dt
import uuid
import hashlib

# ══════════════════════════════════════════
#  기본 설정
# ══════════════════════════════════════════
today = datetime.date.today()

st.set_page_config(
    layout="wide",
    page_title="부산갈매기 · 롯데 자이언츠",
    page_icon="⚾",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════
#  디자인 시스템 (Toss 스타일)
# ══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

/* ─── 기본 ─── */
*, *::before, *::after {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    box-sizing: border-box;
}
.stApp { background: #F2F4F7 !important; }
.main .block-container {
    padding: 1.5rem 2rem 5rem 2rem !important;
    max-width: 1440px !important;
}
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none; }

/* ─── 탭 네비게이션 ─── */
div[data-testid="stTabs"] > div:first-child > div[role="tablist"] {
    background: #FFFFFF !important;
    border-radius: 18px !important;
    padding: 7px !important;
    gap: 4px !important;
    border: 1px solid #E5E8EB !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    margin-bottom: 28px !important;
}
div[data-testid="stTabs"] button[role="tab"] {
    border-radius: 13px !important;
    padding: 10px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #6B7684 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.25s ease !important;
    letter-spacing: -0.1px !important;
}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #3182F6 !important;
    color: #FFFFFF !important;
    box-shadow: 0 3px 12px rgba(49,130,246,0.35) !important;
}
div[data-testid="stTabs"] div[role="tabpanel"] {
    border: none !important;
    padding: 0 !important;
}

/* ─── 히어로 배너 ─── */
.hero {
    background: linear-gradient(135deg, #0C2461 0%, #1E3799 40%, #3182F6 100%);
    border-radius: 28px;
    padding: 44px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 48px rgba(12,36,97,0.35);
}
.hero::before {
    content: "⚾";
    position: absolute;
    right: 52px; top: 50%; transform: translateY(-50%);
    font-size: 136px; opacity: 0.1; line-height: 1;
}
.hero::after {
    content: "";
    position: absolute; top: -80px; right: -80px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.15); backdrop-filter: blur(8px);
    color: rgba(255,255,255,0.92); padding: 5px 14px;
    border-radius: 999px; font-size: 13px; font-weight: 600;
    margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.2);
}
.hero h1 {
    color: #FFFFFF !important; font-size: 36px !important;
    font-weight: 800 !important; margin: 0 0 8px 0 !important;
    letter-spacing: -1px !important; line-height: 1.15 !important;
}
.hero-sub {
    color: rgba(255,255,255,0.65) !important;
    font-size: 16px !important; margin: 0 !important; font-weight: 500 !important;
}
.hero-live {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(239,68,68,0.25); color: #FCA5A5;
    padding: 4px 12px; border-radius: 999px;
    font-size: 12px; font-weight: 700; margin-top: 14px;
    border: 1px solid rgba(239,68,68,0.4);
}
.hero-live::before {
    content: ""; width: 7px; height: 7px; border-radius: 50%;
    background: #EF4444; animation: blink 1.4s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ─── 카드 ─── */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid #F0F2F5;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.card:hover {
    box-shadow: 0 6px 28px rgba(0,0,0,0.09);
    transform: translateY(-1px);
}
.card-title {
    font-size: 17px; font-weight: 700; color: #191F28;
    margin: 0 0 18px 0; display: flex; align-items: center; gap: 8px;
    letter-spacing: -0.3px;
}
.card-title-sm { font-size: 15px; font-weight: 700; color: #191F28; margin: 0 0 14px 0; }

/* ─── 순위 테이블 ─── */
.rank-table { width: 100%; border-collapse: collapse; }
.rank-table th {
    background: #F8F9FB; color: #8B95A1; font-weight: 600;
    padding: 9px 6px; text-align: center; font-size: 11px;
    letter-spacing: 0.3px; border-bottom: 2px solid #F0F2F5;
}
.rank-table td {
    padding: 11px 6px; text-align: center; color: #333D4B;
    border-bottom: 1px solid #F8F9FA; font-size: 13px;
    transition: background 0.15s;
}
.rank-table tr.hl td {
    background: linear-gradient(90deg,#EFF6FF,#F0F9FF);
    color: #1D4ED8; font-weight: 700;
}
.rank-table tr:last-child td { border-bottom: none; }
.rnum {
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%;
    font-size: 11px; font-weight: 700;
}
.rnum-1 { background: #FEF3C7; color: #D97706; }
.rnum-2 { background: #F1F5F9; color: #64748B; }
.rnum-3 { background: #FFF3E0; color: #D4580A; }
.rnum-n { background: #F2F4F7; color: #6B7684; }

/* ─── 게시판 ─── */
.post-row {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px;
    background: white; border: 1px solid #F0F2F5; border-radius: 14px;
    margin-bottom: 8px; transition: all 0.2s ease;
}
.post-row:hover { border-color: #BFDBFE; box-shadow: 0 4px 16px rgba(49,130,246,0.09); transform: translateY(-1px); }
.cat-badge {
    display: inline-flex; align-items: center;
    background: #EFF6FF; color: #2563EB;
    padding: 3px 9px; border-radius: 7px;
    font-size: 11px; font-weight: 700; white-space: nowrap; letter-spacing: 0.2px;
}
.cat-badge.응원 { background: #FEF2F2; color: #DC2626; }
.cat-badge.분석 { background: #F0FDF4; color: #16A34A; }
.cat-badge.질문 { background: #FFF7ED; color: #EA580C; }
.cat-badge.거래 { background: #F5F3FF; color: #7C3AED; }
.post-title-txt {
    font-size: 14px; font-weight: 600; color: #191F28;
    flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.post-meta-txt {
    display: flex; gap: 10px; font-size: 11px; color: #8B95A1;
    font-weight: 500; white-space: nowrap; align-items: center;
}

/* ─── 게시글 상세 ─── */
.post-detail-box {
    background: white; border-radius: 20px;
    padding: 32px; border: 1px solid #F0F2F5;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 12px;
}
.comment-box {
    padding: 14px 0; border-bottom: 1px solid #F8F9FA;
}
.comment-box:last-child { border-bottom: none; }

/* ─── 투표 바 ─── */
.vote-bar-wrap {
    display: flex; height: 52px; border-radius: 14px; overflow: hidden;
    background: #F2F4F7; margin: 10px 0;
}
.vote-lotte {
    background: linear-gradient(90deg,#B91C1C,#EF4444);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 14px;
    transition: width 0.7s cubic-bezier(.4,0,.2,1);
}
.vote-opp {
    background: linear-gradient(90deg,#1D4ED8,#3B82F6);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 800; font-size: 14px; flex: 1;
    transition: width 0.7s cubic-bezier(.4,0,.2,1);
}

/* ─── 버튼 ─── */
div[data-testid="stButton"] button {
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 14px !important; transition: all 0.2s !important;
    letter-spacing: -0.1px !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12) !important;
}

/* ─── 입력 필드 ─── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div > div {
    border: 2px solid #E5E8EB !important; border-radius: 12px !important;
    font-size: 14px !important; transition: border-color 0.2s !important;
    background: #FAFBFC !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 4px rgba(49,130,246,0.1) !important;
    background: white !important;
}

/* ─── 라디오 ─── */
div[data-testid="stRadio"] > label { font-weight: 700 !important; color: #191F28 !important; margin-bottom: 10px !important; }
div[data-testid="stRadio"] div[role="radiogroup"] > label {
    background: #F8F9FA; border: 2px solid #E5E8EB;
    border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;
    cursor: pointer; transition: all 0.2s; font-weight: 600 !important; color: #333D4B !important;
    display: flex !important; align-items: center !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: #EFF6FF; border-color: #3182F6; color: #1D4ED8 !important;
}

/* ─── 링크 버튼 ─── */
div[data-testid="stLinkButton"] a {
    border-radius: 12px !important; font-weight: 700 !important; font-size: 14px !important;
}

/* ─── 선택박스 ─── */
div[data-testid="stSelectbox"] > div { border-radius: 12px !important; }

/* ─── iframe ─── */
iframe { border-radius: 16px !important; }

/* ─── 구분선 ─── */
.toss-hr { border: none; border-top: 1px solid #F0F2F5; margin: 20px 0; }

/* ─── 태그 ─── */
.voter-tag {
    display: inline-flex; align-items: center; gap: 4px;
    background: #F2F4F7; color: #333D4B;
    border-radius: 8px; padding: 5px 11px;
    font-size: 12px; font-weight: 700; margin: 3px;
}

/* ─── 스탯 박스 ─── */
.stat-box {
    background: #F8F9FA; border-radius: 14px;
    padding: 18px 16px; text-align: center;
}
.stat-val { font-size: 30px; font-weight: 800; color: #191F28; line-height: 1; }
.stat-lbl { font-size: 12px; color: #8B95A1; font-weight: 600; margin-top: 5px; }

/* ─── 알림 ─── */
div[data-testid="stAlert"] { border-radius: 12px !important; }

/* ─── Success/Warning ─── */
.stSuccess { border-radius: 12px !important; }

/* ─── 섹션 타이틀 ─── */
.sec-title { font-size: 20px; font-weight: 800; color: #191F28; margin: 0 0 4px 0; letter-spacing: -0.4px; }
.sec-sub { font-size: 14px; color: #8B95A1; margin: 0 0 20px 0; }

/* ─── 빈 상태 ─── */
.empty-state {
    text-align: center; padding: 52px 0; color: #8B95A1;
}
.empty-icon { font-size: 44px; margin-bottom: 12px; }
.empty-title { font-size: 16px; font-weight: 700; color: #4E5968; margin-bottom: 6px; }
.empty-sub { font-size: 13px; }

/* ─── 토스트 메시지 ─── */
div[data-testid="stToast"] { border-radius: 14px !important; }

/* ─── 게임 배지 ─── */
.game-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 13px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.live { background: #FEF2F2; color: #EF4444; border: 1px solid #FCA5A5; }
.live::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: #EF4444; animation: blink 1.4s infinite; display: inline-block; }
.sched { background: #EFF6FF; color: #3B82F6; border: 1px solid #BFDBFE; }
.done { background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  Supabase 초기화
# ══════════════════════════════════════════
SUPABASE_URL = "https://vdltbxhknxhckhakuyin.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkbHRieGhrbnhoY2toYWt1eWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4MzQ3MTgsImV4cCI6MjA2NjQxMDcxOH0.XY07QQtvjjQ2QyR4-FvZGk3yipRs8EGYmHBZ845tUu0"

@st.cache_resource
def get_sb():
    try:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

sb = get_sb()


# ══════════════════════════════════════════
#  세션 상태
# ══════════════════════════════════════════
_defaults = {
    "board_view": "list",       # list | write | detail
    "post_id": None,
    "predict_done": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════
#  유틸리티
# ══════════════════════════════════════════
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def fmt_dt(ts: str, mode="short") -> str:
    if not ts:
        return ""
    try:
        d = dt.fromisoformat(ts.replace("Z", "+00:00"))
        if mode == "short":
            return d.strftime("%m.%d %H:%M")
        return d.strftime("%Y.%m.%d %H:%M")
    except Exception:
        return ts[:16].replace("T", " ")


# ══════════════════════════════════════════
#  데이터 함수
# ══════════════════════════════════════════

# ── KBO 순위 ──
@st.cache_data(ttl=300)
def get_standings():
    try:
        url = "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.tData")
        if not table:
            return None
        df = pd.read_html(str(table))[0]
        rename = {"팀명": "팀"}
        df = df.rename(columns=rename)
        cols = [c for c in ["순위", "팀", "승", "패", "무", "승률", "게임차"] if c in df.columns]
        return df[cols].reset_index(drop=True)
    except Exception:
        return None


# ── 게시판 CRUD ──
def _posts(category="전체"):
    if not sb:
        return []
    try:
        q = sb.table("lotte_posts").select("*").order("created_at", desc=True)
        if category != "전체":
            q = q.eq("category", category)
        return q.execute().data or []
    except Exception:
        return []

def _post(pid):
    if not sb:
        return None
    try:
        return sb.table("lotte_posts").select("*").eq("id", str(pid)).single().execute().data
    except Exception:
        return None

def _create_post(title, content, author, pw, category):
    if not sb:
        return False
    try:
        sb.table("lotte_posts").insert({
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "author": author or "익명",
            "password": hash_pw(pw) if pw else "",
            "category": category,
            "views": 0,
            "likes": 0,
        }).execute()
        return True
    except Exception as e:
        st.error(f"오류: {e}")
        return False

def _delete_post(pid, pw):
    if not sb:
        return False, "DB 연결 오류"
    try:
        post = _post(pid)
        if not post:
            return False, "게시글을 찾을 수 없습니다."
        stored_pw = post.get("password", "")
        if stored_pw and stored_pw != hash_pw(pw):
            return False, "비밀번호가 맞지 않습니다."
        sb.table("lotte_posts").delete().eq("id", str(pid)).execute()
        return True, "삭제됐습니다."
    except Exception as e:
        return False, str(e)

def _inc_views(pid):
    if not sb:
        return
    try:
        post = _post(pid)
        if post:
            sb.table("lotte_posts").update({"views": post.get("views", 0) + 1}).eq("id", str(pid)).execute()
    except Exception:
        pass

def _like_post(pid):
    if not sb:
        return 0
    try:
        post = _post(pid)
        if post:
            nl = post.get("likes", 0) + 1
            sb.table("lotte_posts").update({"likes": nl}).eq("id", str(pid)).execute()
            return nl
    except Exception:
        pass
    return 0

def _comments(pid):
    if not sb:
        return []
    try:
        return sb.table("lotte_comments").select("*").eq("post_id", str(pid)).order("created_at").execute().data or []
    except Exception:
        return []

def _add_comment(pid, author, content):
    if not sb:
        return False
    try:
        sb.table("lotte_comments").insert({
            "id": str(uuid.uuid4()),
            "post_id": str(pid),
            "author": author or "익명",
            "content": content,
        }).execute()
        return True
    except Exception:
        return False


# ── 승부예측 ──
def _today_votes():
    if not sb:
        return pd.DataFrame()
    try:
        res = sb.table("vote_predictions").select("*").eq("vote_date", today.isoformat()).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def _add_vote(nickname, team):
    if not sb:
        return False
    try:
        sb.table("vote_predictions").insert({
            "id": str(uuid.uuid4()),
            "nickname": nickname,
            "selected_team": team,
            "vote_date": today.isoformat(),
        }).execute()
        return True
    except Exception:
        return False


# ══════════════════════════════════════════
#  히어로 배너
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">⚾ 비공식 팬 플랫폼</div>
    <h1>부산갈매기</h1>
    <p class="hero-sub">롯데 자이언츠 팬들이 모이는 곳 · {today.strftime('%Y년 %m월 %d일')}</p>
    <div class="hero-live">LIVE 경기 정보 실시간 업데이트 중</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  탭 네비게이션
# ══════════════════════════════════════════
t_home, t_game, t_board, t_predict = st.tabs([
    "🏠  홈",
    "⚾  경기",
    "📋  게시판",
    "🎯  승부예측",
])


# ════════════════════════════════════════════════════════════
#  🏠 홈 탭
# ════════════════════════════════════════════════════════════
with t_home:
    col_L, col_C, col_R = st.columns([1.3, 2.7, 1.5], gap="medium")

    # ── 왼쪽: KBO 순위 ──
    with col_L:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏆 KBO 리그 순위</div>', unsafe_allow_html=True)

        df = get_standings()
        if df is not None:
            rows_html = ""
            for _, row in df.iterrows():
                rank = str(row.get("순위", ""))
                is_lotte = "롯데" in str(row.get("팀", ""))
                rn_cls = {"1": "rnum-1", "2": "rnum-2", "3": "rnum-3"}.get(rank, "rnum-n")
                cells = f"""
                    <td><span class="rnum {rn_cls}">{rank}</span></td>
                    <td style="text-align:left;padding-left:6px;font-weight:{'800' if is_lotte else '500'}">{row.get("팀","")}</td>
                    <td>{row.get("승","")}</td>
                    <td>{row.get("패","")}</td>
                    <td>{row.get("승률","")}</td>
                    <td style="color:#8B95A1">{row.get("게임차","")}</td>
                """
                rows_html += f'<tr class="{"hl" if is_lotte else ""}">{cells}</tr>'
            st.markdown(f"""
            <table class="rank-table">
                <thead>
                    <tr>
                        <th>순위</th><th style="text-align:left;padding-left:6px">팀</th>
                        <th>승</th><th>패</th><th>승률</th><th>게임차</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📡</div>
                <div class="empty-title">순위를 불러올 수 없어요</div>
                <div class="empty-sub">잠시 후 다시 시도해주세요</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 오늘의 예측 미리보기
        votes = _today_votes()
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎯 오늘의 예측 현황</div>', unsafe_allow_html=True)
        if not votes.empty:
            total = len(votes)
            lotte_n = len(votes[votes["selected_team"] == "롯데"])
            lotte_pct = round(lotte_n / total * 100, 1)
            opp_pct = round(100 - lotte_pct, 1)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700;margin-bottom:6px">
                <span style="color:#EF4444">🔴 롯데 {lotte_pct}%</span>
                <span style="color:#3B82F6">{opp_pct}% 상대팀 💙</span>
            </div>
            <div class="vote-bar-wrap">
                <div class="vote-lotte" style="width:{lotte_pct}%">{"롯데" if lotte_pct>18 else ""}</div>
                <div class="vote-opp">{"상대팀" if opp_pct>18 else ""}</div>
            </div>
            <p style="text-align:center;font-size:12px;color:#8B95A1;margin-top:8px;font-weight:600">
                총 {total}명 참여 중
            </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state" style="padding:20px 0">
                <div class="empty-icon">🗳️</div>
                <div class="empty-title">아직 예측이 없어요</div>
                <div class="empty-sub">승부예측 탭에서 투표하세요!</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 가운데: 경기 일정 + 뉴스 ──
    with col_C:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📅 KBO 경기 일정 & 결과</div>', unsafe_allow_html=True)
        st.components.v1.iframe(
            "https://sports.daum.net/schedule/kbo",
            height=350, scrolling=False
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📰 롯데 자이언츠 최신 뉴스</div>', unsafe_allow_html=True)
        st.components.v1.iframe(
            "https://sports.daum.net/team/kbo/386/news",
            height=340, scrolling=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 오른쪽: 하이라이트 + 예매 ──
    with col_R:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎬 최근 하이라이트</div>', unsafe_allow_html=True)
        st.markdown("**롯데 vs 삼성**")
        st.video("https://youtu.be/VToF__mooJs?si=ViJYOvBfV0RTiduD")
        st.markdown("<br>**롯데 주간 플레이**")
        st.video("https://youtu.be/zNFLJ5o_Sfg?si=GoCT-3TPuiqStHGP")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎟️ 티켓 예매</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size:13px;color:#6B7684;margin-bottom:14px;line-height:1.7">
            일반 예매 오픈:<br>
            경기 <strong style="color:#3182F6">1주일 전 오후 2시</strong>
        </p>
        """, unsafe_allow_html=True)
        st.link_button("🎫 예매 페이지", "https://ticket.giantsclub.com/loginForm.do", use_container_width=True)
        st.link_button("📋 시즌 일정", "https://www.giantsclub.com/html/?pcode=257", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  ⚾ 경기 탭
# ════════════════════════════════════════════════════════════
with t_game:
    gc1, gc2 = st.columns([3, 2], gap="medium")

    with gc1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-title">🎮 실시간 게임센터 & 문자중계
            <span class="game-badge live">LIVE</span>
        </div>
        <p style="font-size:13px;color:#8B95A1;margin-bottom:14px">
            경기 중에는 실시간 문자중계를 확인할 수 있습니다.
        </p>
        """, unsafe_allow_html=True)
        st.components.v1.iframe(
            "https://sports.daum.net/match/80090756",
            height=620, scrolling=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📅 월간 경기 일정</div>', unsafe_allow_html=True)
        st.components.v1.iframe(
            "https://sports.daum.net/schedule/kbo",
            height=380, scrolling=False
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with gc2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎬 하이라이트 영상</div>', unsafe_allow_html=True)
        st.markdown("**▷ 롯데 vs 삼성 하이라이트**")
        st.video("https://youtu.be/VToF__mooJs?si=ViJYOvBfV0RTiduD")
        st.markdown("<br>**▷ 롯데 주간 베스트 플레이**")
        st.video("https://youtu.be/zNFLJ5o_Sfg?si=GoCT-3TPuiqStHGP")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏟️ 사직구장 & 예매</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;flex-direction:column;gap:10px;font-size:14px;color:#4E5968;margin-bottom:16px">
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #F0F2F5">
                <span style="color:#8B95A1;font-weight:600">위치</span>
                <span style="font-weight:700">부산광역시 동래구</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #F0F2F5">
                <span style="color:#8B95A1;font-weight:600">수용 인원</span>
                <span style="font-weight:700">약 24,000명</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:10px 0">
                <span style="color:#8B95A1;font-weight:600">예매 오픈</span>
                <span style="font-weight:700;color:#3182F6">경기 1주 전 14:00</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🎫 티켓 예매", "https://ticket.giantsclub.com/loginForm.do", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  📋 게시판 탭
# ════════════════════════════════════════════════════════════
with t_board:
    CATS = ["자유", "응원", "분석", "질문", "거래"]

    bv = st.session_state.board_view

    # ── 목록 ──
    if bv == "list":
        hc1, hc2 = st.columns([8, 2])
        with hc1:
            st.markdown(f"""
            <p class="sec-title">📋 팬 게시판</p>
            <p class="sec-sub">롯데 자이언츠 팬들과 이야기를 나눠보세요</p>
            """, unsafe_allow_html=True)
        with hc2:
            if st.button("✏️  글쓰기", type="primary", use_container_width=True):
                st.session_state.board_view = "write"
                st.rerun()

        fc1, fc2 = st.columns([3, 9])
        with fc1:
            cat_filter = st.selectbox(
                "카테고리", ["전체"] + CATS,
                label_visibility="collapsed"
            )

        posts = _posts(cat_filter)

        if not sb:
            st.warning("⚠️ Supabase 연결이 필요합니다. `supabase_schema.sql`을 실행하고 설정을 확인하세요.")
        elif not posts:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📝</div>
                <div class="empty-title">아직 게시글이 없어요</div>
                <div class="empty-sub">첫 번째 글을 작성해보세요!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for p in posts:
                pc1, pc2 = st.columns([13, 1])
                with pc1:
                    cat = p.get("category", "자유")
                    st.markdown(f"""
                    <div class="post-row">
                        <span class="cat-badge {cat}">{cat}</span>
                        <span class="post-title-txt">{p.get("title","")}</span>
                        <div class="post-meta-txt">
                            <span>✍️ {p.get("author","익명")}</span>
                            <span>👁 {p.get("views",0)}</span>
                            <span>❤️ {p.get("likes",0)}</span>
                            <span>🕐 {fmt_dt(p.get("created_at",""))}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with pc2:
                    if st.button("읽기", key=f"r_{p['id']}", use_container_width=True):
                        st.session_state.board_view = "detail"
                        st.session_state.post_id = p["id"]
                        _inc_views(p["id"])
                        st.rerun()

    # ── 글쓰기 ──
    elif bv == "write":
        if st.button("← 목록으로 돌아가기"):
            st.session_state.board_view = "list"
            st.rerun()

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">✏️ 새 게시글 작성</div>', unsafe_allow_html=True)

        wc1, wc2 = st.columns([3, 1])
        with wc1:
            w_title = st.text_input("제목 *", placeholder="제목을 입력하세요")
        with wc2:
            w_cat = st.selectbox("카테고리", CATS)

        ac1, ac2 = st.columns(2)
        with ac1:
            w_author = st.text_input("닉네임", placeholder="닉네임 (미입력 시 익명)")
        with ac2:
            w_pw = st.text_input("비밀번호 (삭제용)", type="password", placeholder="나중에 삭제할 때 필요")

        w_content = st.text_area("내용 *", placeholder="내용을 입력하세요...", height=260)

        bc1, bc2, _ = st.columns([2, 2, 6])
        with bc1:
            if st.button("게시하기 →", type="primary", use_container_width=True):
                if not w_title.strip():
                    st.warning("제목을 입력해주세요.")
                elif not w_content.strip():
                    st.warning("내용을 입력해주세요.")
                elif _create_post(w_title.strip(), w_content.strip(), w_author.strip(), w_pw, w_cat):
                    st.success("✅ 게시글이 등록됐습니다!")
                    st.session_state.board_view = "list"
                    st.rerun()
                else:
                    st.error("등록에 실패했습니다. 잠시 후 다시 시도해주세요.")
        with bc2:
            if st.button("취소", use_container_width=True):
                st.session_state.board_view = "list"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 상세 보기 ──
    elif bv == "detail":
        if st.button("← 목록으로 돌아가기"):
            st.session_state.board_view = "list"
            st.session_state.post_id = None
            st.rerun()

        post = _post(st.session_state.post_id)

        if not post:
            st.error("게시글을 찾을 수 없습니다.")
        else:
            cat = post.get("category", "자유")
            st.markdown(f"""
            <div class="post-detail-box">
                <div style="margin-bottom:14px">
                    <span class="cat-badge {cat}">{cat}</span>
                </div>
                <h2 style="font-size:24px;font-weight:800;color:#191F28;margin:0 0 14px;letter-spacing:-0.5px">
                    {post.get("title","")}
                </h2>
                <div style="display:flex;gap:18px;font-size:13px;color:#8B95A1;font-weight:500;margin-bottom:24px;flex-wrap:wrap">
                    <span>✍️ <strong style="color:#4E5968">{post.get("author","익명")}</strong></span>
                    <span>📅 {fmt_dt(post.get("created_at",""), "long")}</span>
                    <span>👁 {post.get("views",0)} 조회</span>
                    <span>❤️ {post.get("likes",0)} 좋아요</span>
                </div>
                <div class="toss-hr"></div>
                <div style="font-size:16px;color:#333D4B;line-height:1.85;white-space:pre-wrap;word-break:break-word">
{post.get("content","")}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 좋아요 & 삭제
            act1, act2, act3 = st.columns([2, 2, 8])
            with act1:
                if st.button(f"❤️  좋아요 ({post.get('likes',0)})", use_container_width=True):
                    _like_post(st.session_state.post_id)
                    st.rerun()
            with act2:
                with st.expander("🗑️  삭제"):
                    dp = st.text_input("삭제 비밀번호", type="password", key="dpw")
                    if st.button("삭제 확인", key="del_btn"):
                        ok, msg = _delete_post(st.session_state.post_id, dp)
                        if ok:
                            st.session_state.board_view = "list"
                            st.session_state.post_id = None
                            st.rerun()
                        else:
                            st.error(msg)

            # 댓글
            comments = _comments(st.session_state.post_id)
            st.markdown('<div class="card" style="margin-top:14px">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-title">💬 댓글 {len(comments)}개</div>', unsafe_allow_html=True)

            if comments:
                for c in comments:
                    st.markdown(f"""
                    <div class="comment-box">
                        <div style="margin-bottom:5px">
                            <span style="font-size:14px;font-weight:700;color:#333D4B">{c.get("author","익명")}</span>
                            <span style="font-size:12px;color:#B0B8C1;margin-left:8px">{fmt_dt(c.get("created_at",""))}</span>
                        </div>
                        <div style="font-size:14px;color:#4E5968;line-height:1.65;word-break:break-word">{c.get("content","")}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <p style="text-align:center;color:#8B95A1;font-size:14px;padding:16px 0">
                    첫 댓글을 남겨보세요! 💬
                </p>
                """, unsafe_allow_html=True)

            st.markdown('<div class="toss-hr"></div>', unsafe_allow_html=True)
            cc1, cc2 = st.columns([1, 3])
            with cc1:
                c_author = st.text_input("닉네임", placeholder="익명", key="ca")
            with cc2:
                c_content = st.text_input("댓글을 입력하세요", placeholder="Enter로 등록", key="cc")

            if st.button("댓글 등록", type="primary"):
                if c_content.strip():
                    _add_comment(st.session_state.post_id, c_author.strip(), c_content.strip())
                    st.rerun()
                else:
                    st.warning("댓글 내용을 입력해주세요.")
            st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  🎯 승부예측 탭
# ════════════════════════════════════════════════════════════
with t_predict:
    votes = _today_votes()
    total = len(votes) if not votes.empty else 0
    lotte_n = len(votes[votes["selected_team"] == "롯데"]) if not votes.empty else 0
    opp_n   = total - lotte_n
    lotte_pct = round(lotte_n / total * 100, 1) if total > 0 else 50.0
    opp_pct   = round(100 - lotte_pct, 1)

    pc1, pc2 = st.columns([5, 7], gap="medium")

    with pc1:
        # 투표 카드
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card-title">🎯 {today.strftime("%m월 %d일")} 오늘 경기 예측</div>
        <div style="background:linear-gradient(135deg,#EFF6FF,#F0F9FF);border-radius:16px;padding:20px;text-align:center;margin-bottom:18px">
            <div style="font-size:28px;margin-bottom:8px">🔴 롯데 <span style="color:#CBD5E1;font-size:20px">vs</span> 상대팀 💙</div>
            <div style="font-size:13px;color:#6B7684;font-weight:600">오늘 경기에서 누가 이길까요?</div>
        </div>
        """, unsafe_allow_html=True)

        if not sb:
            st.warning("⚠️ 데이터베이스 연결이 필요합니다.")
        else:
            p_nick = st.text_input("닉네임 *", placeholder="닉네임을 입력하세요", key="pn")
            p_team = st.radio(
                "예측",
                ["🔴 최강 롯데 자이언츠 이겨라!!", "💙 오늘은 상대팀"],
                label_visibility="visible"
            )

            if st.button("🎯  예측 제출하기", type="primary", use_container_width=True):
                if not p_nick.strip():
                    st.warning("닉네임을 입력해주세요.")
                elif not votes.empty and p_nick.strip() in votes["nickname"].values:
                    st.warning("이미 오늘 예측을 완료했어요! 내일 다시 도전하세요 😊")
                else:
                    team_val = "롯데" if "롯데" in p_team else "상대팀"
                    if _add_vote(p_nick.strip(), team_val):
                        st.success(f"✅ {p_nick.strip()}님의 예측이 등록됐어요!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("등록에 실패했습니다. 잠시 후 다시 시도해주세요.")

        st.markdown('</div>', unsafe_allow_html=True)

        # 통계 카드
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 오늘 참여 통계</div>', unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{total}</div>
                <div class="stat-lbl">총 참여</div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="color:#EF4444">{lotte_n}</div>
                <div class="stat-lbl">롯데 응원</div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="color:#3B82F6">{opp_n}</div>
                <div class="stat-lbl">상대팀 응원</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pc2:
        # 실시간 결과
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 실시간 예측 결과</div>', unsafe_allow_html=True)

        if total > 0:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="font-size:16px;font-weight:800;color:#EF4444">🔴 롯데 {lotte_pct}%</span>
                <span style="font-size:16px;font-weight:800;color:#3B82F6">{opp_pct}% 상대팀 💙</span>
            </div>
            <div class="vote-bar-wrap" style="height:60px;margin-bottom:24px">
                <div class="vote-lotte" style="width:{lotte_pct}%;font-size:16px">{"롯데" if lotte_pct>16 else ""}</div>
                <div class="vote-opp" style="font-size:16px">{"상대팀" if opp_pct>16 else ""}</div>
            </div>
            """, unsafe_allow_html=True)

            # 롯데 응원단
            l_voters = votes[votes["selected_team"] == "롯데"]["nickname"].tolist()
            o_voters = votes[votes["selected_team"] == "상대팀"]["nickname"].tolist()

            if l_voters:
                tags = "".join([f'<span class="voter-tag">⚾ {n}</span>' for n in l_voters])
                st.markdown(f"""
                <div style="margin-bottom:18px">
                    <p style="font-size:14px;font-weight:800;color:#EF4444;margin-bottom:8px">🔴 롯데 응원단 ({len(l_voters)}명)</p>
                    <div>{tags}</div>
                </div>
                """, unsafe_allow_html=True)

            if o_voters:
                tags = "".join([f'<span class="voter-tag">💙 {n}</span>' for n in o_voters])
                st.markdown(f"""
                <div>
                    <p style="font-size:14px;font-weight:800;color:#3B82F6;margin-bottom:8px">💙 상대팀 응원단 ({len(o_voters)}명)</p>
                    <div>{tags}</div>
                </div>
                """, unsafe_allow_html=True)

            # 응원 메시지
            if lotte_pct > 60:
                msg = f"오늘은 팬들의 {lotte_pct}%가 롯데를 응원하고 있어요! 이길 것 같은 느낌이 팍팍!! 💪"
                color = "#EF4444"
            elif lotte_pct < 40:
                msg = f"팬들의 {opp_pct}%가 상대팀을 응원하네요. 롯데가 역전의 명수임을 보여줄 시간! ⚡"
                color = "#3B82F6"
            else:
                msg = "팬들도 오늘 경기는 반반! 어느 팀이 이길지 모르는 명승부가 예상됩니다 🔥"
                color = "#F59E0B"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#F8F9FA,#F2F4F7);border-radius:14px;
                        padding:16px;margin-top:20px;border-left:4px solid {color}">
                <p style="font-size:14px;color:#333D4B;margin:0;font-weight:600;line-height:1.6">{msg}</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="empty-state" style="padding:60px 0">
                <div class="empty-icon">🎯</div>
                <div class="empty-title">아직 예측이 없어요</div>
                <div class="empty-sub">첫 번째 예측자가 되어보세요!<br>왼쪽에서 예측을 입력해보세요 👈</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
#  푸터
# ══════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:40px 0 20px;color:#B0B8C1;font-size:13px;font-weight:500;line-height:1.8">
    ⚾ 부산갈매기 · 롯데 자이언츠 비공식 팬 플랫폼<br>
    <span style="font-size:12px;color:#D1D5DB">모든 데이터는 KBO 공식 홈페이지 및 다음 스포츠를 기반으로 합니다</span>
</div>
""", unsafe_allow_html=True)
