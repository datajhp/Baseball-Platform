import streamlit as st
import datetime
import requests
from datetime import datetime as dt, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import uuid

# ─────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────
today = datetime.date.today()
today_str = today.strftime('%Y%m%d')

st.set_page_config(
    layout="wide",
    page_title="롯데 자이언츠 데일리",
    page_icon="⚾"
)

# ─────────────────────────────────────────────
# 토스 디자인 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

*, *::before, *::after {
    box-sizing: border-box;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* 전체 배경 */
.stApp {
    background-color: #F2F4F7 !important;
}

/* 헤더 숨기기 */
header[data-testid="stHeader"] {
    background: transparent;
}

/* 메인 패딩 */
.main .block-container {
    padding: 2rem 2rem 4rem 2rem !important;
    max-width: 1400px !important;
}

/* 히어로 헤더 */
.toss-hero {
    background: linear-gradient(135deg, #1A47B8 0%, #3182F6 60%, #4B9FFA 100%);
    border-radius: 24px;
    padding: 36px 40px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(49, 130, 246, 0.28);
}
.toss-hero::before {
    content: "⚾";
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 96px;
    opacity: 0.15;
}
.toss-hero h1 {
    color: white !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    margin: 0 0 6px 0 !important;
    letter-spacing: -0.5px;
}
.toss-hero p {
    color: rgba(255,255,255,0.75) !important;
    font-size: 15px !important;
    margin: 0 !important;
}

/* 카드 공통 스타일 */
.toss-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    border: 1px solid #F0F2F5;
    transition: box-shadow 0.2s ease;
}
.toss-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
}

/* 카드 타이틀 */
.toss-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #191F28;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 날씨 상태 배지 */
.weather-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EFF6FF;
    color: #1D4ED8;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 16px;
}

/* 날씨 정보 행 */
.weather-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0;
    border-bottom: 1px solid #F2F4F7;
    font-size: 15px;
}
.weather-row:last-child { border-bottom: none; }
.weather-label { color: #6B7684; font-weight: 500; }
.weather-value { color: #191F28; font-weight: 700; }

/* 경기 확률 카드 */
.prob-card {
    background: linear-gradient(135deg, #F0F7FF 0%, #EBF4FF 100%);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #BFDBFE;
    margin-top: 16px;
}
.prob-title {
    font-size: 14px;
    color: #6B7684;
    font-weight: 600;
    margin-bottom: 4px;
}
.prob-value {
    font-size: 36px;
    font-weight: 800;
    color: #1D4ED8;
    line-height: 1.1;
}
.prob-comment {
    font-size: 13px;
    color: #4B6CB7;
    margin-top: 6px;
    font-weight: 500;
}

/* 순위 테이블 */
.rank-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.rank-table th {
    background: #F8F9FA;
    color: #6B7684;
    font-weight: 600;
    padding: 10px 8px;
    text-align: center;
    border-bottom: 2px solid #F0F2F5;
}
.rank-table td {
    padding: 10px 8px;
    text-align: center;
    color: #191F28;
    border-bottom: 1px solid #F8F9FA;
}
.rank-table tr.lotte-row td {
    background: #EFF6FF;
    color: #1D4ED8;
    font-weight: 700;
}
.rank-table tr:hover td {
    background: #FAFBFC;
}

/* 예측 투표 */
.vote-bar-wrap {
    background: #F2F4F7;
    border-radius: 12px;
    overflow: hidden;
    height: 48px;
    display: flex;
    margin-top: 12px;
}
.vote-bar-lotte {
    background: linear-gradient(90deg, #EF4444, #F97316);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 14px;
    transition: width 0.5s ease;
}
.vote-bar-opponent {
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 14px;
    flex: 1;
    transition: width 0.5s ease;
}

/* 구분선 */
.toss-divider {
    border: none;
    border-top: 1px solid #E5E8EB;
    margin: 28px 0;
}

/* 섹션 타이틀 */
.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #191F28;
    margin: 0 0 16px 0;
    letter-spacing: -0.3px;
}

/* 예측자 태그 */
.voter-tag {
    display: inline-flex;
    align-items: center;
    background: #F2F4F7;
    color: #333D4B;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 13px;
    font-weight: 600;
    margin: 3px;
}

/* Streamlit 기본 위젯 스타일 재정의 */
div[data-testid="stTextInput"] input {
    border: 2px solid #E5E8EB !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    font-size: 15px !important;
    transition: border-color 0.2s !important;
    background: white !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 4px rgba(49,130,246,0.12) !important;
}

/* 버튼 */
div[data-testid="stButton"] button {
    background: #3182F6 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    transition: all 0.2s !important;
    width: 100%;
}
div[data-testid="stButton"] button:hover {
    background: #1A6EE8 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(49,130,246,0.35) !important;
}

/* 라디오 버튼 */
div[data-testid="stRadio"] label {
    font-size: 15px !important;
    color: #333D4B !important;
    font-weight: 600 !important;
}

/* 링크 버튼 */
div[data-testid="stLinkButton"] a {
    background: #191F28 !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    text-decoration: none !important;
    display: inline-block !important;
}

/* iframe 컨테이너 */
iframe {
    border-radius: 16px !important;
    border: 1px solid #E5E8EB !important;
}

/* 알림 박스 */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 히어로 헤더
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="toss-hero">
    <h1>롯데 자이언츠 데일리 ⚾</h1>
    <p>{today.strftime('%Y년 %m월 %d일')} · 오늘의 경기 정보, 날씨, 순위를 한눈에</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 유틸 함수들
# ─────────────────────────────────────────────
pty_map = {
    "0": ("☀️", "맑음"),
    "1": ("🌧️", "비"),
    "2": ("🌨️", "비/눈"),
    "3": ("❄️", "눈"),
    "4": ("⛈️", "소나기"),
    "5": ("💧", "빗방울"),
    "6": ("🌦️", "빗방울/눈날림"),
    "7": ("🌨️", "눈날림"),
}

def get_current_weather():
    service_key = "UXqugk+0AxpQyJqlQtC3Ebew3mFF6rvXVzErFuMm/0g7zMMAndYGFHjkPkcMK1LBSM+wEs8d3hslVgSWeSOoqw=="
    nx, ny = 98, 76
    now = dt.now()
    base_date = now.strftime('%Y%m%d')
    base_time = (now - timedelta(minutes=40)).strftime('%H') + "00"
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "100",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    try:
        res = requests.get(url, params=params, timeout=5, verify=True)
        res.raise_for_status()
        items = res.json()["response"]["body"]["items"]["item"]
        return {i["category"]: i["obsrValue"] for i in items}
    except Exception:
        return {}

def get_kbo_rankings():
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.tData")
        if not table:
            return None
        df = pd.read_html(str(table))[0]
        df = df.rename(columns={"순위": "순위", "팀명": "팀", "승": "승", "패": "패",
                                  "무": "무", "승률": "승률", "게임차": "게임차"})
        return df[["순위", "팀", "승", "패", "무", "승률", "게임차"]].reset_index(drop=True)
    except Exception:
        return None


# ─────────────────────────────────────────────
# 섹션 1: 일정 + 순위 + 날씨
# ─────────────────────────────────────────────
col_sched, col_side = st.columns([6, 4], gap="medium")

with col_sched:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">📅 오늘의 KBO 경기 일정</div>', unsafe_allow_html=True)
    st.components.v1.iframe(
        src="https://sports.daum.net/schedule/kbo",
        width=None, height=460, scrolling=False
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # KBO 순위
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">🏆 KBO 리그 순위</div>', unsafe_allow_html=True)
    df_rank = get_kbo_rankings()
    if df_rank is not None:
        rows_html = ""
        for _, row in df_rank.iterrows():
            is_lotte = "롯데" in str(row.get("팀", ""))
            tr_class = 'class="lotte-row"' if is_lotte else ""
            cells = "".join([f"<td>{v}</td>" for v in row])
            rows_html += f"<tr {tr_class}>{cells}</tr>"
        headers_html = "".join([f"<th>{c}</th>" for c in df_rank.columns])
        st.markdown(f"""
        <table class="rank-table">
            <thead><tr>{headers_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.info("순위 데이터를 불러오지 못했습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 날씨 카드
    current = get_current_weather()
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">🏟️ 사직구장 현재 날씨</div>', unsafe_allow_html=True)

    if current:
        pty_code = current.get("PTY", "0")
        icon, summary = pty_map.get(pty_code, ("🌈", "정보없음"))
        temp = current.get("T1H", "-")
        humidity = current.get("REH", "-")
        wind = current.get("WSD", "-")
        rain = current.get("RN1", "0")

        st.markdown(f"""
        <div class="weather-badge">{icon} {summary}</div>
        <div class="weather-row">
            <span class="weather-label">🌡️ 기온</span>
            <span class="weather-value">{temp} °C</span>
        </div>
        <div class="weather-row">
            <span class="weather-label">💧 습도</span>
            <span class="weather-value">{humidity} %</span>
        </div>
        <div class="weather-row">
            <span class="weather-label">🌬️ 풍속</span>
            <span class="weather-value">{wind} m/s</span>
        </div>
        <div class="weather-row">
            <span class="weather-label">☔ 강수량(1h)</span>
            <span class="weather-value">{rain} mm</span>
        </div>
        """, unsafe_allow_html=True)

        # 경기 진행 확률
        try:
            rain_f = float(rain)
            temp_f = float(temp)
            wind_f = float(wind)
            score = 100
            if rain_f > 10: score -= 40
            elif rain_f > 3: score -= 25
            elif rain_f > 1: score -= 10
            if temp_f < 5 or temp_f > 33: score -= 10
            if wind_f > 7: score -= 10
            score = max(30, min(score, 100))

            if score > 90:   comment = "야구하기 완벽한 날씨! 오늘 꼭 이겨라! 💪"
            elif score > 75: comment = "경기 가능! 함 해봐!"
            elif score > 60: comment = "다소 흐리지만 경기는 진행됩니다"
            elif score > 45: comment = "유동적 — 우산 챙기세요 ☂️"
            else:            comment = "우천 취소 가능성 있음 ⛔"

            color = "#10B981" if score > 75 else "#F59E0B" if score > 50 else "#EF4444"
            st.markdown(f"""
            <div class="prob-card">
                <div class="prob-title">경기 진행 예상 확률</div>
                <div class="prob-value" style="color:{color}">{score}%</div>
                <div class="prob-comment">{comment}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            pass
    else:
        st.warning("날씨 데이터를 불러오지 못했습니다.")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 구분선
# ─────────────────────────────────────────────
st.markdown('<hr class="toss-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 섹션 2: 뉴스 + 하이라이트/예매
# ─────────────────────────────────────────────
col_news, col_yt = st.columns([6, 4], gap="medium")

with col_news:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">📰 롯데 자이언츠 최신 뉴스</div>', unsafe_allow_html=True)
    st.components.v1.iframe(
        src="https://sports.daum.net/team/kbo/386/news",
        width=None, height=560, scrolling=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_yt:
    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">🎬 최근 경기 하이라이트</div>', unsafe_allow_html=True)
    st.markdown("**롯데 vs 삼성 하이라이트**")
    st.video("https://youtu.be/VToF__mooJs?si=ViJYOvBfV0RTiduD")
    st.markdown("**롯데 자이언츠 주간 플레이 모음**")
    st.video("https://youtu.be/zNFLJ5o_Sfg?si=GoCT-3TPuiqStHGP")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="toss-card">', unsafe_allow_html=True)
    st.markdown('<div class="toss-card-title">🎟️ 티켓 예매</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#6B7684; font-size:14px; margin-bottom:12px;">
        일반 예매 오픈: 경기 1주일 전 <strong style="color:#3182F6">오후 2시</strong>
    </p>
    """, unsafe_allow_html=True)
    st.link_button("▶ 예매 페이지 바로가기", "https://ticket.giantsclub.com/loginForm.do")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 구분선
# ─────────────────────────────────────────────
st.markdown('<hr class="toss-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 섹션 3: 실시간 중계
# ─────────────────────────────────────────────
st.markdown('<div class="toss-card">', unsafe_allow_html=True)
st.markdown('<div class="toss-card-title">🎮 실시간 게임 센터</div>', unsafe_allow_html=True)
st.markdown("""
<p style="color:#6B7684; font-size:14px; margin-bottom:12px;">
    경기 시간에 맞추면 실시간 중계를 확인할 수 있습니다.
</p>
""", unsafe_allow_html=True)
st.components.v1.iframe(
    src="https://sports.daum.net/match/80090756",
    width=None, height=720, scrolling=True
)
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 구분선
# ─────────────────────────────────────────────
st.markdown('<hr class="toss-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 섹션 4: 승부 예측
# ─────────────────────────────────────────────
try:
    from supabase import create_client, Client

    SUPABASE_URL = "https://vdltbxhknxhckhakuyin.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkbHRieGhrbnhoY2toYWt1eWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4MzQ3MTgsImV4cCI6MjA2NjQxMDcxOH0.XY07QQtvjjQ2QyR4-FvZGk3yipRs8EGYmHBZ845tUu0"
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    st.markdown(f"""
    <div class="section-title">⚾ {today.strftime('%m월 %d일')} 승부 예측</div>
    """, unsafe_allow_html=True)

    col_vote, col_result = st.columns([4, 6], gap="medium")

    with col_vote:
        st.markdown('<div class="toss-card">', unsafe_allow_html=True)
        st.markdown('<div class="toss-card-title">🗳️ 오늘 누가 이길까요?</div>', unsafe_allow_html=True)

        nickname = st.text_input("닉네임", placeholder="닉네임을 입력하세요")
        selected = st.radio(
            "예측 선택",
            ("최강 롯데 자이언츠 🔴", "상대팀 💙"),
            label_visibility="collapsed"
        )

        if st.button("예측 제출하기 →"):
            if nickname.strip():
                team_value = "롯데" if "롯데" in selected else "상대팀"
                supabase.table("vote_predictions").insert({
                    "id": str(uuid.uuid4()),
                    "nickname": nickname.strip(),
                    "selected_team": team_value,
                    "vote_date": today.isoformat()
                }).execute()
                st.success(f"✅ {nickname}님의 예측이 등록됐어요!")
            else:
                st.warning("닉네임을 입력해주세요.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="toss-card">', unsafe_allow_html=True)
        st.markdown('<div class="toss-card-title">📊 실시간 예측 현황</div>', unsafe_allow_html=True)

        res = supabase.table("vote_predictions").select("*").eq("vote_date", today.isoformat()).execute()
        votes = pd.DataFrame(res.data) if res.data else pd.DataFrame()

        if not votes.empty:
            count_df = votes["selected_team"].value_counts().reset_index()
            count_df.columns = ["팀", "득표수"]
            total = count_df["득표수"].sum()
            count_df["득표율"] = (count_df["득표수"] / total * 100).round(1)

            lotte_pct = float(count_df[count_df["팀"] == "롯데"]["득표율"].values[0]) if "롯데" in count_df["팀"].values else 0
            opp_pct = round(100 - lotte_pct, 1)

            st.markdown(f"""
            <div style="margin-bottom:8px; display:flex; justify-content:space-between; font-size:14px; font-weight:700;">
                <span style="color:#EF4444">롯데 {lotte_pct}%</span>
                <span style="color:#3B82F6">상대팀 {opp_pct}%</span>
            </div>
            <div class="vote-bar-wrap">
                <div class="vote-bar-lotte" style="width:{lotte_pct}%">
                    {"롯데" if lotte_pct > 20 else ""}
                </div>
                <div class="vote-bar-opponent" style="width:{opp_pct}%">
                    {"상대팀" if opp_pct > 20 else ""}
                </div>
            </div>
            <div style="margin-top:6px; font-size:13px; color:#6B7684; text-align:right;">
                총 {total}명 참여
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            for team_name, color in [("롯데", "#EF4444"), ("상대팀", "#3B82F6")]:
                team_votes = votes[votes["selected_team"] == team_name]["nickname"].tolist()
                if team_votes:
                    tags = "".join([f'<span class="voter-tag">{n}</span>' for n in team_votes])
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="font-size:13px; color:{color}; font-weight:700; margin-bottom:6px;">
                            {"🔴 롯데 팀" if team_name=="롯데" else "💙 상대팀"}
                        </div>
                        <div>{tags}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:32px 0; color:#6B7684;">
                <div style="font-size:32px; margin-bottom:8px;">🗳️</div>
                <div style="font-weight:600; font-size:15px;">아직 예측이 없어요</div>
                <div style="font-size:13px; margin-top:4px;">첫 번째 예측자가 되어보세요!</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

except ImportError:
    st.info("supabase 패키지가 설치되지 않아 예측 기능을 불러올 수 없습니다. requirements.txt를 확인하세요.")
except Exception as e:
    st.error(f"예측 기능 오류: {e}")
