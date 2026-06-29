import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    try:
        url = "https://www.koreabaseball.com/ws/Main.asmx/GetKboStandings"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://www.koreabaseball.com",
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers, json={}, timeout=10)
        print(f"상태코드: {res.status_code}")
        print(f"응답내용: {res.text[:500]}")

        data = res.json()
        teams = data.get("d", [])

        lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]
        medals = ["🥇", "🥈", "🥉"]

        for i, team in enumerate(teams[:10]):
            name = team.get("TEAM_NM", "")
            win  = team.get("W", "")
            lose = team.get("L", "")
            draw = team.get("D", "")
            pct  = team.get("WRA", "")
            gb   = team.get("GB", "")
            icon = medals[i] if i < 3 else f"{i+1}위"
            lines.append(f"{icon} {name}  {win}승 {lose}패 {draw}무  승률 {pct}  게임차 {gb}")

        if len(lines) > 1:
            return "\n".join(lines)

    except Exception as e:
        print(f"실패: {e}")

    return "❌ 순위 데이터를 가져오지 못했어요."

message = get_kbo_standings()
print(message)
requests.post(WEBHOOK_URL, json={"content": message})
print(f"전송 완료: {datetime.now()}")
