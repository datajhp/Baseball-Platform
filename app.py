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
import json
import re
import xml.etree.ElementTree as ET

today = datetime.date.today()

st.set_page_config(
    layout="wide",
    page_title="부산갈매기 · 롯데 자이언츠",
    page_icon="⚾",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*,*::before,*::after{font-family:'Pretendard',-apple-system,BlinkMacSystemFont,sans-serif!important;box-sizing:border-box}
.stApp{background:#F2F4F7!important}
.main .block-container{padding:1.5rem 2rem 5rem 2rem!important;max-width:1440px!important}
header[data-testid="stHeader"]{background:transparent!important}
section[data-testid="stSidebar"]{display:none!important}
div[data-testid="stTabs"]>div:first-child>div[role="tablist"]{background:#fff!important;border-radius:18px!important;padding:7px!important;gap:4px!important;border:1px solid #E5E8EB!important;box-shadow:0 2px 12px rgba(0,0,0,.06)!important;margin-bottom:28px!important}
div[data-testid="stTabs"] button[role="tab"]{border-radius:13px!important;padding:10px 22px!important;font-size:15px!important;font-weight:600!important;color:#6B7684!important;border:none!important;background:transparent!important;transition:all .25s!important}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{background:#3182F6!important;color:#fff!important;box-shadow:0 3px 12px rgba(49,130,246,.35)!important}
div[data-testid="stTabs"] div[role="tabpanel"]{border:none!important;padding:0!important}
.hero{background:linear-gradient(135deg,#0C2461 0%,#1E3799 40%,#3182F6 100%);border-radius:28px;padding:44px 52px;margin-bottom:32px;position:relative;overflow:hidden;box-shadow:0 16px 48px rgba(12,36,97,.35)}
.hero::before{content:"⚾";position:absolute;right:52px;top:50%;transform:translateY(-50%);font-size:136px;opacity:.1;line-height:1}
.hero-eyebrow{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.15);color:rgba(255,255,255,.92);padding:5px 14px;border-radius:999px;font-size:13px;font-weight:600;margin-bottom:14px;border:1px solid rgba(255,255,255,.2)}
.hero h1{color:#fff!important;font-size:36px!important;font-weight:800!important;margin:0 0 8px 0!important;letter-spacing:-1px!important}
.hero-sub{color:rgba(255,255,255,.65)!important;font-size:16px!important;margin:0!important}
.hero-live{display:inline-flex;align-items:center;gap:7px;background:rgba(239,68,68,.25);color:#FCA5A5;padding:5px 13px;border-radius:999px;font-size:12px;font-weight:700;margin-top:14px;border:1px solid rgba(239,68,68,.4)}
.ldot{width:7px;height:7px;border-radius:50%;background:#EF4444;animation:blink 1.4s infinite;display:inline-block}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.card{background:#fff;border-radius:20px;padding:24px;border:1px solid #F0F2F5;box-shadow:0 2px 12px rgba(0,0,0,.04);margin-bottom:20px;transition:box-shadow .2s,transform .2s}
.card:hover{box-shadow:0 6px 28px rgba(0,0,0,.09);transform:translateY(-1px)}
.card-title{font-size:17px;font-weight:700;color:#191F28;margin:0 0 18px 0;display:flex;align-items:center;gap:8px;letter-spacing:-.3px}
.rank-table{width:100%;border-collapse:collapse}
.rank-table th{background:#F8F9FB;color:#8B95A1;font-weight:600;padding:9px 6px;text-align:center;font-size:11px;letter-spacing:.3px;border-bottom:2px solid #F0F2F5}
.rank-table td{padding:11px 6px;text-align:center;color:#333D4B;border-bottom:1px solid #F8F9FA;font-size:13px}
.rank-table tr.hl td{background:linear-gradient(90deg,#EFF6FF,#F0F9FF);color:#1D4ED8;font-weight:700}
.rank-table tr:last-child td{border-bottom:none}
.rnum{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;font-size:11px;font-weight:700}
.rnum-1{background:#FEF3C7;color:#D97706}.rnum-2{background:#F1F5F9;color:#64748B}.rnum-3{background:#FFF3E0;color:#D4580A}.rnum-n{background:#F2F4F7;color:#6B7684}
.game-card{background:white;border:1px solid #F0F2F5;border-radius:16px;padding:18px 20px;margin-bottom:10px;display:flex;align-items:center;gap:16px;transition:all .2s}
.game-card:hover{border-color:#BFDBFE;box-shadow:0 4px 16px rgba(49,130,246,.09)}
.game-card.lc{border-left:4px solid #EF4444}
.score-box{background:#F8F9FA;border-radius:10px;padding:8px 18px;font-size:20px;font-weight:900;color:#191F28;letter-spacing:4px;text-align:center}
.sb{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700}
.sb-live{background:#FEF2F2;color:#EF4444;border:1px solid #FCA5A5}
.sb-sched{background:#EFF6FF;color:#3B82F6;border:1px solid #BFDBFE}
.sb-done{background:#F0FDF4;color:#16A34A;border:1px solid #BBF7D0}
.news-item{padding:13px 0;border-bottom:1px solid #F2F4F7;display:flex;align-items:flex-start;gap:12px}
.news-item:last-child{border-bottom:none}
.news-num{min-width:22px;height:22px;border-radius:6px;background:#F2F4F7;color:#8B95A1;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-top:2px}
.news-title a{font-size:14px;font-weight:600;color:#191F28;line-height:1.5;text-decoration:none}
.news-title a:hover{color:#3182F6}
.news-press{font-size:11px;color:#B0B8C1;font-weight:500;margin-top:3px}
.yt-card{background:white;border:1px solid #F0F2F5;border-radius:16px;overflow:hidden;margin-bottom:14px;transition:all .2s;text-decoration:none;display:block}
.yt-card:hover{box-shadow:0 6px 24px rgba(0,0,0,.1);transform:translateY(-2px)}
.yt-thumb{width:100%;aspect-ratio:16/9;object-fit:cover}
.yt-info{padding:12px 14px}
.yt-ttl{font-size:13px;font-weight:700;color:#191F28;line-height:1.5;margin-bottom:5px}
.yt-meta{font-size:11px;color:#8B95A1;font-weight:500}
.post-row{display:flex;align-items:center;gap:12px;padding:14px 16px;background:white;border:1px solid #F0F2F5;border-radius:14px;margin-bottom:8px;transition:all .2s}
.post-row:hover{border-color:#BFDBFE;box-shadow:0 4px 16px rgba(49,130,246,.09);transform:translateY(-1px)}
.cat-b{display:inline-flex;align-items:center;padding:3px 9px;border-radius:7px;font-size:11px;font-weight:700;white-space:nowrap}
.cat-자유{background:#EFF6FF;color:#2563EB}.cat-응원{background:#FEF2F2;color:#DC2626}.cat-분석{background:#F0FDF4;color:#16A34A}.cat-질문{background:#FFF7ED;color:#EA580C}.cat-거래{background:#F5F3FF;color:#7C3AED}
.post-ttl{font-size:14px;font-weight:600;color:#191F28;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.post-meta{display:flex;gap:10px;font-size:11px;color:#8B95A1;font-weight:500;white-space:nowrap;align-items:center}
.vote-wrap{display:flex;height:52px;border-radius:14px;overflow:hidden;background:#F2F4F7;margin:10px 0}
.vote-l{background:linear-gradient(90deg,#B91C1C,#EF4444);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:14px}
.vote-o{background:linear-gradient(90deg,#1D4ED8,#3B82F6);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:14px;flex:1}
.stat-box{background:#F8F9FA;border-radius:14px;padding:18px 16px;text-align:center}
.stat-val{font-size:30px;font-weight:800;color:#191F28;line-height:1}
.stat-lbl{font-size:12px;color:#8B95A1;font-weight:600;margin-top:5px}
.vtag{display:inline-flex;align-items:center;gap:4px;background:#F2F4F7;color:#333D4B;border-radius:8px;padding:5px 11px;font-size:12px;font-weight:700;margin:3px}
.hr{border:none;border-top:1px solid #F0F2F5;margin:18px 0}
.empty{text-align:center;padding:40px 0;color:#8B95A1}
.empty-i{font-size:40px;margin-bottom:10px}
.empty-t{font-size:15px;font-weight:700;color:#4E5968;margin-bottom:5px}
.empty-s{font-size:13px}
.post-detail{background:white;border-radius:20px;padding:32px;border:1px solid #F0F2F5;box-shadow:0 2px 12px rgba(0,0,0,.04);margin-bottom:12px}
.cmt{padding:14px 0;border-bottom:1px solid #F8F9FA}
.cmt:last-child{border-bottom:none}
div[data-testid="stButton"] button{border-radius:12px!important;font-weight:700!important;font-size:14px!important;transition:all .2s!important}
div[data-testid="stButton"] button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(0,0,0,.12)!important}
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea{border:2px solid #E5E8EB!important;border-radius:12px!important;font-size:14px!important;background:#FAFBFC!important;transition:border-color .2s!important}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus{border-color:#3182F6!important;box-shadow:0 0 0 4px rgba(49,130,246,.1)!important;background:white!important}
div[data-testid="stLinkButton"] a{border-radius:12px!important;font-weight:700!important}
div[data-testid="stAlert"]{border-radius:12px!important}
/* ── 라디오 버튼 텍스트 가시성 명시 강제 ── */
div[data-testid="stRadio"] label {
    color: #191F28 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
div[data-testid="stRadio"] > div > label {
    color: #191F28 !important;
}
div[data-testid="stRadio"] p,
div[data-testid="stRadio"] span {
    color: #191F28 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
/* 라디오 선택지 레이아웃 */
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
}
div[data-testid="stRadio"] > div > label {
    background: #F8F9FA !important;
    border: 2px solid #E5E8EB !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: #3182F6 !important;
    background: #EFF6FF !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #EFF6FF !important;
    border-color: #3182F6 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Supabase
@st.cache_resource
def get_sb():
    try:
        from supabase import create_client
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except Exception:
        return None

sb = get_sb()

for k, v in {"board_view": "list", "post_id": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


# ══════════════════════════════════════════
#  스크래핑 함수
# ══════════════════════════════════════════
@st.cache_data(ttl=300)
def get_standings():
    try:
        res = requests.get("https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx", headers=HDR, timeout=10)
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


@st.cache_data(ttl=120)
def get_today_games():
    """KBO 오늘 경기 — 네이버 스포츠 파싱 (가장 안정적)"""
    today_str = today.strftime('%Y%m%d')
    games = []

    # ── 소스 1: 네이버 스포츠 KBO 일정
    try:
        url = f"https://sports.news.naver.com/kbaseball/schedule/index?date={today_str}"
        res = requests.get(url, headers=HDR, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # 오늘 날짜 경기만 추출
        for row in soup.select("table.schedule_table tbody tr, table tbody tr"):
            cols = row.select("td")
            if len(cols) < 3:
                continue
            texts = [c.get_text(strip=True) for c in cols]
            full = " ".join(texts)
            # 팀명 포함 여부로 경기 행 판단
            kbo_teams = ["롯데","삼성","LG","두산","KT","SSG","한화","NC","KIA","키움"]
            if sum(1 for t in kbo_teams if t in full) >= 2:
                # 팀 추출 (포함된 팀들 찾기)
                found = [t for t in kbo_teams if t in full]
                away = found[0] if len(found) > 0 else ""
                home = found[1] if len(found) > 1 else ""
                # 점수 패턴
                score_match = re.search(r'(\d+)\s*[:\-]\s*(\d+)', full)
                score = f"{score_match.group(1)}:{score_match.group(2)}" if score_match else "vs"
                # 시간 패턴
                time_match = re.search(r'(\d{1,2}:\d{2})', full)
                time_s = time_match.group(1) if time_match else ""
                # 구장
                stadiums = ["사직","잠실","수원","대전","고척","창원","광주","대구","인천","포항"]
                stad = next((s for s in stadiums if s in full), "")
                # 상태
                state = ""
                if "종료" in full or "경기종료" in full:
                    state = "종료"
                elif "취소" in full:
                    state = "취소"
                elif score_match and score != "vs":
                    state = "진행중"

                games.append({
                    "away": away, "home": home, "score": score,
                    "time": time_s, "stadium": stad, "state": state,
                    "is_lotte": "롯데" in away or "롯데" in home,
                })
    except Exception:
        pass

    # ── 소스 2: KBO 공식 Schedule 페이지 (fallback)
    if not games:
        try:
            url = f"https://www.koreabaseball.com/Schedule/Schedule.aspx"
            res = requests.get(url, headers=HDR, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            kbo_teams = ["롯데","삼성","LG","두산","KT","SSG","한화","NC","KIA","키움"]

            for table in soup.select("table"):
                rows = table.select("tr")
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.select("td")]
                    if not cols:
                        continue
                    full = " ".join(cols)
                    found = [t for t in kbo_teams if t in full]
                    if len(found) >= 2:
                        score_match = re.search(r'(\d+)\s*[:\-]\s*(\d+)', full)
                        time_match  = re.search(r'(\d{1,2}:\d{2})', full)
                        stadiums = ["사직","잠실","수원","대전","고척","창원","광주","대구","인천"]
                        games.append({
                            "away": found[0], "home": found[1],
                            "score": f"{score_match.group(1)}:{score_match.group(2)}" if score_match else "vs",
                            "time": time_match.group(1) if time_match else "",
                            "stadium": next((s for s in stadiums if s in full), ""),
                            "state": "종료" if "종료" in full else "",
                            "is_lotte": "롯데" in found,
                        })
                if games:
                    break
        except Exception:
            pass

    # ── 소스 3: KBO 공식 JSON API (최후 fallback)
    if not games:
        try:
            url = f"https://www.koreabaseball.com/ws/Main.asmx/GetKBOGameList"
            payload = {"leId": "1", "srId": "0,1,3,4,5,7,8,9", "date": today_str}
            res = requests.post(url, data=payload, headers={**HDR, "Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
            data = res.json()
            kbo_teams = {"LT": "롯데", "SS": "삼성", "LG": "LG", "OB": "두산",
                         "KT": "KT",  "SK": "SSG", "HH": "한화", "NC": "NC",
                         "HT": "KIA", "WO": "키움"}
            for g in data.get("game", []):
                away_cd = g.get("visitTeamCode", "")
                home_cd = g.get("homeTeamCode", "")
                away = kbo_teams.get(away_cd, away_cd)
                home = kbo_teams.get(home_cd, home_cd)
                vs = g.get("visitScore","")
                hs = g.get("homeScore","")
                score = f"{vs}:{hs}" if vs != "" and hs != "" else "vs"
                games.append({
                    "away": away, "home": home, "score": score,
                    "time": g.get("gtime",""), "stadium": g.get("stadium",""),
                    "state": g.get("status",""),
                    "is_lotte": "롯데" in [away, home],
                })
        except Exception:
            pass

    return games


@st.cache_data(ttl=300)
def get_lotte_news():
    """Google News RSS로 롯데 자이언츠 뉴스"""
    try:
        url = "https://news.google.com/rss/search?q=롯데+자이언츠&hl=ko&gl=KR&ceid=KR:ko"
        res = requests.get(url, headers=HDR, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.text)
        news = []
        for item in root.findall(".//item")[:10]:
            title_el  = item.find("title")
            link_el   = item.find("link")
            source_el = item.find("source")
            pub_el    = item.find("pubDate")
            title = re.sub(r'\s*-\s*[^-]+$', '', title_el.text or "").strip() if title_el is not None else ""
            link  = link_el.text or "" if link_el is not None else ""
            press = source_el.text or "" if source_el is not None else ""
            pub   = (pub_el.text or "")[:16] if pub_el is not None else ""
            if title:
                news.append({"title": title, "url": link, "press": press, "pub": pub})
        return news
    except Exception:
        return []


@st.cache_data(ttl=1800)
def get_youtube_highlights():
    """YouTube 검색에서 최신 롯데 하이라이트 동적으로 가져오기"""
    try:
        query = "롯데+자이언츠+하이라이트"
        url = f"https://www.youtube.com/results?search_query={query}&sp=CAI%3D"
        res = requests.get(url, headers=HDR, timeout=15)
        res.raise_for_status()
        match = re.search(r'ytInitialData\s*=\s*({.+?});\s*</script>', res.text)
        if not match:
            return []
        data = json.loads(match.group(1))
        sections = (data.get("contents", {})
                        .get("twoColumnSearchResultsRenderer", {})
                        .get("primaryContents", {})
                        .get("sectionListRenderer", {})
                        .get("contents", []))
        videos = []
        for section in sections:
            for item in section.get("itemSectionRenderer", {}).get("contents", []):
                vr = item.get("videoRenderer", {})
                if not vr:
                    continue
                vid_id = vr.get("videoId", "")
                title  = (vr.get("title", {}).get("runs") or [{}])[0].get("text", "")
                ch     = (vr.get("ownerText", {}).get("runs") or [{}])[0].get("text", "")
                pub    = vr.get("publishedTimeText", {}).get("simpleText", "")
                thumbs = vr.get("thumbnail", {}).get("thumbnails", [])
                thumb  = thumbs[-1].get("url", "") if thumbs else f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
                if vid_id and title:
                    videos.append({"id": vid_id, "title": title, "channel": ch, "time": pub, "thumb": thumb})
                if len(videos) >= 4:
                    return videos
        return videos
    except Exception:
        return []


# ══════════════════════════════════════════
#  DB 유틸
# ══════════════════════════════════════════
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def fmt_dt(ts, mode="short"):
    if not ts: return ""
    try:
        d = dt.fromisoformat(ts.replace("Z", "+00:00"))
        return d.strftime("%m.%d %H:%M") if mode == "short" else d.strftime("%Y.%m.%d %H:%M")
    except Exception:
        return str(ts)[:16].replace("T", " ")

def _posts(cat="전체"):
    if not sb: return []
    try:
        q = sb.table("lotte_posts").select("*").order("created_at", desc=True)
        if cat != "전체": q = q.eq("category", cat)
        return q.execute().data or []
    except Exception: return []

def _post(pid):
    if not sb: return None
    try: return sb.table("lotte_posts").select("*").eq("id", str(pid)).single().execute().data
    except Exception: return None

def _create_post(title, content, author, pw, cat):
    if not sb: return False
    try:
        sb.table("lotte_posts").insert({
            "id": str(uuid.uuid4()), "title": title, "content": content,
            "author": author or "익명", "password": hash_pw(pw) if pw else "",
            "category": cat, "views": 0, "likes": 0,
        }).execute()
        return True
    except Exception as e:
        st.error(f"등록 오류: {e}"); return False

def _delete_post(pid, pw):
    if not sb: return False, "DB 연결 오류"
    try:
        post = _post(pid)
        if not post: return False, "게시글을 찾을 수 없습니다."
        if post.get("password") and post["password"] != hash_pw(pw): return False, "비밀번호가 맞지 않습니다."
        sb.table("lotte_posts").delete().eq("id", str(pid)).execute()
        return True, "삭제됐습니다."
    except Exception as e: return False, str(e)

def _inc_views(pid):
    if not sb: return
    try:
        p = _post(pid)
        if p: sb.table("lotte_posts").update({"views": p.get("views", 0) + 1}).eq("id", str(pid)).execute()
    except Exception: pass

def _like_post(pid):
    if not sb: return 0
    try:
        p = _post(pid)
        if p:
            nl = p.get("likes", 0) + 1
            sb.table("lotte_posts").update({"likes": nl}).eq("id", str(pid)).execute()
            return nl
    except Exception: return 0

def _comments(pid):
    if not sb: return []
    try: return sb.table("lotte_comments").select("*").eq("post_id", str(pid)).order("created_at").execute().data or []
    except Exception: return []

def _add_comment(pid, author, content):
    if not sb: return False
    try:
        sb.table("lotte_comments").insert({"id": str(uuid.uuid4()), "post_id": str(pid), "author": author or "익명", "content": content}).execute()
        return True
    except Exception: return False

def _today_votes():
    if not sb: return pd.DataFrame()
    try:
        res = sb.table("vote_predictions").select("*").eq("vote_date", today.isoformat()).execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception: return pd.DataFrame()

def _add_vote(nick, team):
    if not sb: return False
    try:
        sb.table("vote_predictions").insert({"id": str(uuid.uuid4()), "nickname": nick, "selected_team": team, "vote_date": today.isoformat()}).execute()
        return True
    except Exception: return False


# ══════════════════════════════════════════
#  히어로
# ══════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">⚾ 비공식 팬 플랫폼</div>
    <h1>부산갈매기</h1>
    <p class="hero-sub">롯데 자이언츠 팬들이 모이는 곳 · {today.strftime('%Y년 %m월 %d일')}</p>
    <div class="hero-live"><span class="ldot"></span>경기 정보 실시간 업데이트 중</div>
</div>
""", unsafe_allow_html=True)


t_home, t_game, t_board, t_predict = st.tabs(["🏠  홈", "⚾  경기", "📋  게시판", "🎯  승부예측"])


# ════════════════════════════════
#  🏠 홈
# ════════════════════════════════
with t_home:
    standings   = get_standings()
    today_games = get_today_games()
    news_list   = get_lotte_news()
    highlights  = get_youtube_highlights()
    votes       = _today_votes()

    cL, cC, cR = st.columns([1.4, 2.8, 1.5], gap="medium")

    with cL:
        # 순위
        st.markdown('<div class="card"><div class="card-title">🏆 KBO 리그 순위</div>', unsafe_allow_html=True)
        if standings is not None:
            rows_html = ""
            for _, row in standings.iterrows():
                rank = str(row.get("순위",""))
                is_l = "롯데" in str(row.get("팀",""))
                rc = {"1":"rnum-1","2":"rnum-2","3":"rnum-3"}.get(rank,"rnum-n")
                rows_html += f'<tr class="{"hl" if is_l else ""}"><td><span class="rnum {rc}">{rank}</span></td><td style="text-align:left;padding-left:6px;font-weight:{"800" if is_l else "500"}">{row.get("팀","")}</td><td>{row.get("승","")}</td><td>{row.get("패","")}</td><td>{row.get("승률","")}</td><td style="color:#8B95A1">{row.get("게임차","")}</td></tr>'
            st.markdown(f'<table class="rank-table"><thead><tr><th>순위</th><th style="text-align:left;padding-left:6px">팀</th><th>승</th><th>패</th><th>승률</th><th>게임차</th></tr></thead><tbody>{rows_html}</tbody></table>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty"><div class="empty-i">📡</div><div class="empty-t">순위 로딩 실패</div><div class="empty-s">새로고침 해주세요</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 예측 미리보기
        st.markdown('<div class="card"><div class="card-title">🎯 오늘의 예측 현황</div>', unsafe_allow_html=True)
        tv = len(votes)
        if not votes.empty and tv > 0:
            ln = len(votes[votes["selected_team"]=="롯데"])
            lp = round(ln/tv*100, 1); op = round(100-lp, 1)
            st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700;margin-bottom:6px"><span style="color:#EF4444">🔴 롯데 {lp}%</span><span style="color:#3B82F6">{op}% 상대팀 💙</span></div><div class="vote-wrap"><div class="vote-l" style="width:{lp}%">{"롯데" if lp>18 else ""}</div><div class="vote-o">{"상대팀" if op>18 else ""}</div></div><p style="text-align:center;font-size:12px;color:#8B95A1;margin-top:8px;font-weight:600">총 {tv}명 참여 중</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:20px 0"><div class="empty-i">🗳️</div><div class="empty-t">아직 예측이 없어요</div><div class="empty-s">승부예측 탭에서 투표하세요!</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cC:
        # 오늘 경기
        st.markdown(f'<div class="card"><div class="card-title">📅 오늘의 KBO 경기 <span style="font-size:13px;color:#8B95A1;font-weight:500">· {today.strftime("%m/%d")}</span></div>', unsafe_allow_html=True)
        if today_games:
            for g in today_games:
                aw, hm = g.get("away",""), g.get("home","")
                sc = g.get("score","vs")
                ti = g.get("time","")
                stad = g.get("stadium","")
                sta = g.get("state","")
                is_l = g.get("is_lotte", False)
                if "종료" in sta or "완료" in sta:
                    bdg = '<span class="sb sb-done">종료</span>'
                elif sta and sta not in ["-",""]:
                    bdg = '<span class="sb sb-live"><span class="ldot" style="width:6px;height:6px"></span>진행중</span>'
                else:
                    bdg = f'<span class="sb sb-sched">{ti}</span>'
                st.markdown(f'<div class="game-card {"lc" if is_l else ""}"><div style="flex:1"><div style="display:flex;align-items:center;justify-content:center;gap:16px"><span style="font-size:15px;font-weight:{"900" if is_l else "600"};color:#191F28;min-width:64px;text-align:right">{aw}</span><span class="score-box">{sc}</span><span style="font-size:15px;font-weight:{"900" if is_l else "600"};color:#191F28;min-width:64px">{hm}</span></div><div style="text-align:center;margin-top:8px;display:flex;gap:8px;justify-content:center;align-items:center">{bdg}<span style="font-size:12px;color:#B0B8C1">{stad}</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="empty" style="padding:28px 0"><div class="empty-i">🌙</div><div class="empty-t">경기 정보를 불러오지 못했어요</div><div class="empty-s">아래 버튼에서 직접 확인해보세요</div></div>', unsafe_allow_html=True)
        st.link_button("📋 네이버 스포츠에서 오늘 경기 확인", f"https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime('%Y%m%d')}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 뉴스
        st.markdown('<div class="card"><div class="card-title">📰 롯데 자이언츠 최신 뉴스</div>', unsafe_allow_html=True)
        if news_list:
            for i, n in enumerate(news_list[:8], 1):
                st.markdown(f'<div class="news-item"><span class="news-num">{i}</span><div style="flex:1"><div class="news-title"><a href="{n["url"]}" target="_blank">{n["title"]}</a></div><div class="news-press">{n.get("press","")} · {n.get("pub","")}</div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:24px 0"><div class="empty-i">📡</div><div class="empty-t">뉴스를 불러오지 못했어요</div></div>', unsafe_allow_html=True)
        st.link_button("🔗 네이버 스포츠 뉴스", "https://sports.news.naver.com/kbaseball/news/index?type=team&teamCode=LT", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cR:
        # 하이라이트
        st.markdown('<div class="card"><div class="card-title">🎬 최신 하이라이트</div>', unsafe_allow_html=True)
        if highlights:
            for v in highlights[:2]:
                vid = v["id"]
                thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                st.markdown(f'<a class="yt-card" href="https://www.youtube.com/watch?v={vid}" target="_blank"><img class="yt-thumb" src="{thumb}" onerror="this.src=\'https://img.youtube.com/vi/{vid}/hqdefault.jpg\'" alt=""><div class="yt-info"><div class="yt-ttl">{v.get("title","")[:52]}</div><div class="yt-meta">{v.get("channel","")} · {v.get("time","")}</div></div></a>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:20px 0"><div class="empty-i">🎬</div><div class="empty-t">영상 로딩 실패</div></div>', unsafe_allow_html=True)
        st.link_button("▶ YouTube 더보기", "https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 예매
        st.markdown('<div class="card"><div class="card-title">🎟️ 티켓 예매</div><p style="font-size:13px;color:#6B7684;margin-bottom:14px;line-height:1.7">일반 예매 오픈:<br>경기 <strong style="color:#3182F6">1주일 전 오후 2시</strong></p>', unsafe_allow_html=True)
        st.link_button("🎫 예매 페이지", "https://ticket.giantsclub.com/loginForm.do", use_container_width=True)
        st.link_button("📋 시즌 일정", "https://www.giantsclub.com/html/?pcode=257", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════
#  ⚾ 경기
# ════════════════════════════════
with t_game:
    tg = get_today_games()
    hl = get_youtube_highlights()
    lotte_g = [g for g in tg if g.get("is_lotte")]

    gc1, gc2 = st.columns([3, 2], gap="medium")
    with gc1:
        st.markdown('<div class="card"><div class="card-title">⚾ 오늘 롯데 자이언츠 경기</div>', unsafe_allow_html=True)
        if lotte_g:
            g = lotte_g[0]
            aw, hm = g.get("away",""), g.get("home","")
            sc = g.get("score","vs"); ti = g.get("time",""); stad = g.get("stadium",""); sta = g.get("state","")
            is_live = sta and "종료" not in sta and sta not in ["-",""]
            sbdg = '<span class="sb sb-live"><span class="ldot" style="width:6px;height:6px"></span>진행중</span>' if is_live else f'<span class="sb sb-sched">{ti}</span>'
            st.markdown(f'<div style="background:linear-gradient(135deg,#EFF6FF,#F0F9FF);border-radius:18px;padding:28px;text-align:center;margin-bottom:18px"><div style="margin-bottom:12px">{sbdg}</div><div style="display:flex;align-items:center;justify-content:center;gap:24px"><div><div style="font-size:24px;font-weight:900;color:#191F28">{aw}</div><div style="font-size:12px;color:#8B95A1;margin-top:3px">원정</div></div><div style="font-size:36px;font-weight:900;color:#191F28;letter-spacing:6px;padding:12px 24px;background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,.06)">{sc}</div><div><div style="font-size:24px;font-weight:900;color:#191F28">{hm}</div><div style="font-size:12px;color:#8B95A1;margin-top:3px">홈</div></div></div><div style="margin-top:14px;font-size:13px;color:#8B95A1;font-weight:600">🏟️ {stad}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:32px 0"><div class="empty-i">🌙</div><div class="empty-t">오늘 롯데 경기 정보를 불러오지 못했어요</div><div class="empty-s">아래 버튼에서 직접 확인해보세요</div></div>', unsafe_allow_html=True)
        st.link_button("📋 네이버 스포츠 오늘 경기", f"https://sports.news.naver.com/kbaseball/schedule/index?date={today.strftime('%Y%m%d')}", use_container_width=True)

        st.markdown('<div class="card"><div class="card-title">📡 실시간 문자 중계 <span class="sb sb-live" style="font-size:11px;padding:3px 9px"><span class="ldot" style="width:6px;height:6px"></span>LIVE</span></div><p style="font-size:13px;color:#8B95A1;margin-bottom:14px">경기 중일 때 실시간 중계를 확인할 수 있습니다</p>', unsafe_allow_html=True)
        st.components.v1.iframe("https://sports.daum.net/match/80090756", height=500, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with gc2:
        st.markdown('<div class="card"><div class="card-title">📋 오늘 전체 경기</div>', unsafe_allow_html=True)
        if tg:
            for g in tg:
                aw, hm = g.get("away",""), g.get("home","")
                sc = g.get("score","vs"); sta = g.get("state",""); is_l = g.get("is_lotte",False)
                st.markdown(f'<div class="game-card {"lc" if is_l else ""}" style="padding:13px 16px"><div style="flex:1;display:flex;align-items:center;justify-content:space-between;gap:10px"><span style="font-size:14px;font-weight:{"800" if is_l else "600"};color:#191F28;min-width:48px;text-align:right">{aw}</span><span style="background:#F8F9FA;border-radius:8px;padding:6px 14px;font-size:16px;font-weight:900;color:#191F28;letter-spacing:3px">{sc}</span><span style="font-size:14px;font-weight:{"800" if is_l else "600"};color:#191F28;min-width:48px">{hm}</span><span style="font-size:11px;color:#8B95A1">{sta}</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:24px 0"><div class="empty-i">📅</div><div class="empty-t">오늘은 경기가 없어요</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🎬 최신 하이라이트</div>', unsafe_allow_html=True)
        if hl:
            for v in hl[:3]:
                vid = v["id"]; thumb = v.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                st.markdown(f'<a href="https://www.youtube.com/watch?v={vid}" target="_blank" style="text-decoration:none"><div class="game-card" style="padding:12px"><img src="{thumb}" style="width:110px;height:66px;object-fit:cover;border-radius:8px;flex-shrink:0" onerror="this.src=\'https://img.youtube.com/vi/{vid}/hqdefault.jpg\'" alt=""><div><div style="font-size:12px;font-weight:700;color:#191F28;line-height:1.5">{v.get("title","")[:46]}</div><div style="font-size:11px;color:#8B95A1;margin-top:3px">{v.get("channel","")} · {v.get("time","")}</div></div></div></a>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:20px 0"><div class="empty-i">🎬</div><div class="empty-t">영상을 불러오지 못했어요</div></div>', unsafe_allow_html=True)
        st.link_button("▶ YouTube 더보기", "https://www.youtube.com/results?search_query=롯데+자이언츠+하이라이트&sp=CAI%3D", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════
#  📋 게시판
# ════════════════════════════════
with t_board:
    CATS = ["자유","응원","분석","질문","거래"]
    bv = st.session_state.board_view

    if bv == "list":
        hc1, hc2 = st.columns([8,2])
        with hc1:
            st.markdown('<p style="font-size:20px;font-weight:800;color:#191F28;margin:0 0 4px">📋 팬 게시판</p><p style="font-size:14px;color:#8B95A1;margin:0 0 20px">롯데 자이언츠 팬들과 이야기를 나눠보세요</p>', unsafe_allow_html=True)
        with hc2:
            if st.button("✏️  글쓰기", type="primary", use_container_width=True):
                st.session_state.board_view = "write"; st.rerun()
        fc1, _ = st.columns([2,8])
        with fc1:
            cf = st.selectbox("", ["전체"]+CATS, label_visibility="collapsed")
        posts = _posts(cf)
        if not sb:
            st.warning("⚠️ Supabase 연결이 필요합니다. `.streamlit/secrets.toml`을 설정하세요.")
        elif not posts:
            st.markdown('<div class="empty"><div class="empty-i">📝</div><div class="empty-t">아직 게시글이 없어요</div><div class="empty-s">첫 번째 글을 작성해보세요!</div></div>', unsafe_allow_html=True)
        else:
            for p in posts:
                cat = p.get("category","자유")
                pc1, pc2 = st.columns([13,1])
                with pc1:
                    st.markdown(f'<div class="post-row"><span class="cat-b cat-{cat}">{cat}</span><span class="post-ttl">{p.get("title","")}</span><div class="post-meta"><span>✍️ {p.get("author","익명")}</span><span>👁 {p.get("views",0)}</span><span>❤️ {p.get("likes",0)}</span><span>🕐 {fmt_dt(p.get("created_at",""))}</span></div></div>', unsafe_allow_html=True)
                with pc2:
                    if st.button("읽기", key=f"r_{p['id']}", use_container_width=True):
                        st.session_state.board_view = "detail"; st.session_state.post_id = p["id"]; _inc_views(p["id"]); st.rerun()

    elif bv == "write":
        if st.button("← 목록으로"):
            st.session_state.board_view = "list"; st.rerun()
        st.markdown('<div class="card"><div class="card-title">✏️ 새 게시글 작성</div>', unsafe_allow_html=True)
        wc1, wc2 = st.columns([3,1])
        with wc1: wt = st.text_input("제목 *", placeholder="제목을 입력하세요")
        with wc2: wcat = st.selectbox("카테고리", CATS)
        ac1, ac2 = st.columns(2)
        with ac1: wa = st.text_input("닉네임", placeholder="미입력 시 익명")
        with ac2: wpw = st.text_input("삭제 비밀번호", type="password", placeholder="삭제할 때 필요")
        wc = st.text_area("내용 *", placeholder="내용을 입력하세요...", height=260)
        bc1, bc2, _ = st.columns([2,2,6])
        with bc1:
            if st.button("게시하기 →", type="primary", use_container_width=True):
                if not wt.strip(): st.warning("제목을 입력해주세요.")
                elif not wc.strip(): st.warning("내용을 입력해주세요.")
                elif _create_post(wt.strip(), wc.strip(), wa.strip(), wpw, wcat):
                    st.success("✅ 게시글이 등록됐습니다!"); st.session_state.board_view = "list"; st.rerun()
        with bc2:
            if st.button("취소", use_container_width=True):
                st.session_state.board_view = "list"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif bv == "detail":
        if st.button("← 목록으로"):
            st.session_state.board_view = "list"; st.session_state.post_id = None; st.rerun()
        post = _post(st.session_state.post_id)
        if not post:
            st.error("게시글을 찾을 수 없습니다.")
        else:
            cat = post.get("category","자유")
            st.markdown(f'<div class="post-detail"><span class="cat-b cat-{cat}" style="margin-bottom:14px;display:inline-block">{cat}</span><h2 style="font-size:24px;font-weight:800;color:#191F28;margin:0 0 14px;letter-spacing:-.5px">{post.get("title","")}</h2><div style="display:flex;gap:18px;font-size:13px;color:#8B95A1;font-weight:500;margin-bottom:24px;flex-wrap:wrap"><span>✍️ <strong style="color:#4E5968">{post.get("author","익명")}</strong></span><span>📅 {fmt_dt(post.get("created_at",""),"long")}</span><span>👁 {post.get("views",0)}</span><span>❤️ {post.get("likes",0)}</span></div><div class="hr"></div><div style="font-size:16px;color:#333D4B;line-height:1.85;white-space:pre-wrap;word-break:break-word">{post.get("content","")}</div></div>', unsafe_allow_html=True)
            a1, a2, _ = st.columns([2,2,8])
            with a1:
                if st.button(f"❤️ 좋아요 ({post.get('likes',0)})", use_container_width=True):
                    _like_post(st.session_state.post_id); st.rerun()
            with a2:
                with st.expander("🗑️ 삭제"):
                    dp = st.text_input("삭제 비밀번호", type="password", key="dpw")
                    if st.button("삭제 확인"):
                        ok, msg = _delete_post(st.session_state.post_id, dp)
                        if ok: st.session_state.board_view="list"; st.session_state.post_id=None; st.rerun()
                        else: st.error(msg)
            cmts = _comments(st.session_state.post_id)
            st.markdown(f'<div class="card" style="margin-top:14px"><div class="card-title">💬 댓글 {len(cmts)}개</div>', unsafe_allow_html=True)
            for c in cmts:
                st.markdown(f'<div class="cmt"><span style="font-size:14px;font-weight:700;color:#333D4B">{c.get("author","익명")}</span><span style="font-size:12px;color:#B0B8C1;margin-left:8px">{fmt_dt(c.get("created_at",""))}</span><div style="font-size:14px;color:#4E5968;line-height:1.65;margin-top:5px;word-break:break-word">{c.get("content","")}</div></div>', unsafe_allow_html=True)
            if not cmts:
                st.markdown('<p style="text-align:center;color:#8B95A1;font-size:14px;padding:16px 0">첫 댓글을 남겨보세요! 💬</p>', unsafe_allow_html=True)
            st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
            cc1, cc2 = st.columns([1,3])
            with cc1: ca = st.text_input("닉네임", placeholder="익명", key="ca")
            with cc2: cc = st.text_input("댓글을 입력하세요", key="cc")
            if st.button("댓글 등록", type="primary"):
                if cc.strip(): _add_comment(st.session_state.post_id, ca.strip(), cc.strip()); st.rerun()
                else: st.warning("댓글 내용을 입력해주세요.")
            st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════
#  🎯 승부예측
# ════════════════════════════════
with t_predict:
    votes = _today_votes()
    tp = len(votes)
    ln = len(votes[votes["selected_team"]=="롯데"]) if not votes.empty else 0
    on = tp - ln
    lp = round(ln/tp*100, 1) if tp > 0 else 50.0
    op = round(100-lp, 1)

    pc1, pc2 = st.columns([5,7], gap="medium")
    with pc1:
        st.markdown(f'<div class="card"><div class="card-title">🎯 {today.strftime("%m월 %d일")} 승부 예측</div><div style="background:linear-gradient(135deg,#EFF6FF,#F0F9FF);border-radius:16px;padding:20px;text-align:center;margin-bottom:18px"><div style="font-size:26px;margin-bottom:8px">🔴 롯데 <span style="color:#CBD5E1;font-size:18px">vs</span> 상대팀 💙</div><div style="font-size:13px;color:#6B7684;font-weight:600">오늘 경기 승자를 예측해보세요!</div></div>', unsafe_allow_html=True)
        if not sb:
            st.warning("⚠️ 데이터베이스 연결이 필요합니다.")
        else:
            pn = st.text_input("닉네임 *", placeholder="닉네임을 입력하세요", key="pn")
            pt = st.radio("예측", ["🔴 최강 롯데 자이언츠 이겨라!!", "💙 오늘은 상대팀"])
            if st.button("🎯  예측 제출하기", type="primary", use_container_width=True):
                if not pn.strip(): st.warning("닉네임을 입력해주세요.")
                elif not votes.empty and pn.strip() in votes["nickname"].values: st.warning("이미 오늘 예측을 완료했어요! 😊")
                else:
                    tv = "롯데" if "롯데" in pt else "상대팀"
                    if _add_vote(pn.strip(), tv): st.success(f"✅ {pn.strip()}님의 예측이 등록됐어요!"); st.balloons(); st.rerun()
                    else: st.error("등록에 실패했습니다.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-title">📊 오늘 참여 통계</div>', unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.markdown(f'<div class="stat-box"><div class="stat-val">{tp}</div><div class="stat-lbl">총 참여</div></div>', unsafe_allow_html=True)
        with sc2: st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#EF4444">{ln}</div><div class="stat-lbl">롯데 응원</div></div>', unsafe_allow_html=True)
        with sc3: st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:#3B82F6">{on}</div><div class="stat-lbl">상대팀 응원</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with pc2:
        st.markdown('<div class="card"><div class="card-title">📊 실시간 예측 결과</div>', unsafe_allow_html=True)
        if tp > 0:
            st.markdown(f'<div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:16px;font-weight:800;color:#EF4444">🔴 롯데 {lp}%</span><span style="font-size:16px;font-weight:800;color:#3B82F6">{op}% 상대팀 💙</span></div><div class="vote-wrap" style="height:60px;margin-bottom:24px"><div class="vote-l" style="width:{lp}%;font-size:16px">{"롯데" if lp>16 else ""}</div><div class="vote-o" style="font-size:16px">{"상대팀" if op>16 else ""}</div></div>', unsafe_allow_html=True)
            lv = votes[votes["selected_team"]=="롯데"]["nickname"].tolist()
            ov = votes[votes["selected_team"]=="상대팀"]["nickname"].tolist()
            if lv:
                tags = "".join([f'<span class="vtag">⚾ {n}</span>' for n in lv])
                st.markdown(f'<p style="font-size:14px;font-weight:800;color:#EF4444;margin-bottom:8px">🔴 롯데 응원단 ({len(lv)}명)</p><div style="margin-bottom:16px">{tags}</div>', unsafe_allow_html=True)
            if ov:
                tags = "".join([f'<span class="vtag">💙 {n}</span>' for n in ov])
                st.markdown(f'<p style="font-size:14px;font-weight:800;color:#3B82F6;margin-bottom:8px">💙 상대팀 응원단 ({len(ov)}명)</p><div>{tags}</div>', unsafe_allow_html=True)
            color = "#EF4444" if lp>60 else "#3B82F6" if lp<40 else "#F59E0B"
            msg = f"팬들의 {lp}%가 롯데를 응원해요! 이길 것 같은 느낌! 💪" if lp>60 else f"팬들의 {op}%가 상대팀 응원. 역전의 명수 롯데 파이팅! ⚡" if lp<40 else "팽팽한 예측! 명승부가 예상됩니다 🔥"
            st.markdown(f'<div style="background:#F8F9FA;border-radius:14px;padding:16px;margin-top:20px;border-left:4px solid {color}"><p style="font-size:14px;color:#333D4B;margin:0;font-weight:600;line-height:1.6">{msg}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:60px 0"><div class="empty-i">🎯</div><div class="empty-t">아직 예측이 없어요</div><div class="empty-s">첫 번째 예측자가 되어보세요! 👈</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center;padding:40px 0 20px;color:#B0B8C1;font-size:13px;font-weight:500;line-height:1.8">⚾ 부산갈매기 · 롯데 자이언츠 비공식 팬 플랫폼<br><span style="font-size:12px;color:#D1D5DB">데이터 출처: KBO 공식, Google News, YouTube</span></div>', unsafe_allow_html=True)
