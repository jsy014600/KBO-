import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    try:
        url = "https://site.api.espn.com/apis/v2/sports/baseball/kbo/standings"
        res = requests.get(url, timeout=10)
        print(f"상태코드: {res.status_code}")
        print(f"응답: {res.text[:300]}")
        
        data = res.json()
        groups = data.get("children", [{}])[0].get("standings", {}).get("entries", [])
        print(f"팀 수: {len(groups)}")

        lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]
        medals = ["🥇", "🥈", "🥉"]

        for i, entry in enumerate(groups[:10]):
            team = entry.get("team", {}).get("displayName", "")
            stats = {s["name"]: s["displayValue"] for s in entry.get("stats", [])}
            win  = stats.get("wins", "")
            lose = stats.get("losses", "")
            pct  = stats.get("winPercent", "")
            gb   = stats.get("gamesBehind", "0")
            icon = medals[i] if i < 3 else f"{i+1}위"
            lines.append(f"{icon} {team}  {win}승 {lose}패  승률 {pct}  게임차 {gb}")

        if len(lines) > 1:
            return "\n".join(lines)

    except Exception as e:
        print(f"오류: {e}")

    return "❌ 순위 데이터를 가져오지 못했어요."

message = get_kbo_standings()
print(f"최종메시지: {message[:100]}")
import sys
sys.stdout.flush()
requests.post(WEBHOOK_URL, json={"content": message})
print(f"전송 완료: {datetime.now()}")
sys.stdout.flush()
