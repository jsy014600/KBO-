import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    try:
        url = "https://site.api.espn.com/apis/v2/sports/baseball/kbo/standings"
        res = requests.get(url, timeout=10)
        print(f"상태코드: {res.status_code}")
        data = res.json()

        lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]
        medals = ["🥇", "🥈", "🥉"]

        groups = data.get("children", [{}])[0].get("standings", {}).get("entries", [])
        for i, entry in enumerate(groups[:10]):
            team = entry.get("team", {}).get("displayName", "")
            stats = {s["name"]: s["displayValue"] for s in entry.get("stats", [])}
            win  = stats.get("wins", "")
            lose = stats.get("losses", "")
            pct  = stats.get("winPercent", "")
            gb   = stats.get("gamesBehind", "")
            icon = medals[i] if i < 3 else f"{i+1}위"
            lines.append(f"{icon} {team}  {win}승 {lose}패  승률 {pct}  게임차 {gb}")

        if len(lines) > 1:
            return "\n".join(lines)

    except Exception
