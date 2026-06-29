import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.koreabaseball.com"
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("#tblTeamRank tbody tr")
    lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]

    medals = ["🥇", "🥈", "🥉"]
    for i, row in enumerate(rows[:10]):
        cols = row.select("td")
        if len(cols) < 7:
            continue
        team = cols[1].get_text(strip=True)
        win  = cols[2].get_text(strip=True)
        lose = cols[3].get_text(strip=True)
        draw = cols[4].get_text(strip=True)
        pct  = cols[5].get_text(strip=True)
        gb   = cols[6].get_text(strip=True)
        icon = medals[i] if i < 3 else f"{i+1}위"
        lines.append(f"{icon} {team}  {win}승 {lose}패 {draw}무  승률 {pct}  게임차 {gb}")

    if len(lines) == 1:
        lines.append("❌ 순위 데이터를 가져오지 못했어요.")

    return "\n".join(lines)

message = get_kbo_standings()
requests.post(WEBHOOK_URL, json={"content": message})
print(f"전송 완료: {datetime.now()}")
