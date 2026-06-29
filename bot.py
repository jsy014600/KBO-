import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    # 방법 1: KBO 모바일 사이트 시도
    try:
        url = "https://m.koreabaseball.com/Kbo/TeamRank.aspx"
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table tbody tr")

        lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]
        medals = ["🥇", "🥈", "🥉"]

        for i, row in enumerate(rows[:10]):
            cols = row.select("td")
            if len(cols) < 6:
                continue
            team = cols[1].get_text(strip=True)
            win  = cols[2].get_text(strip=True)
            lose = cols[3].get_text(strip=True)
            pct  = cols[5].get_text(strip=True)
            icon = medals[i] if i < 3 else f"{i+1}위"
            lines.append(f"{icon} {team}  {win}승 {lose}패  승률 {pct}")

        if len(lines) > 1:
            return "\n".join(lines)
    except Exception as e:
        print(f"방법1 실패: {e}")

    # 방법 2: 다음 스포츠 시도
    try:
        url = "https://sports.daum.net/record/kbo"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table tbody tr")

        lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]
        medals = ["🥇", "🥈", "🥉"]

        for i, row in enumerate(rows[:10]):
            cols = row.select("td")
            if len(cols) < 6:
                continue
            team = cols[1].get_text(strip=True)
            win  = cols[2].get_text(strip=True)
            lose = cols[3].get_text(strip=True)
            pct  = cols[5].get_text(strip=True)
            icon = medals[i] if i < 3 else f"{i+1}위"
            lines.append(f"{icon} {team}  {win}승 {lose}패  승률 {pct}")

        if len(lines) > 1:
            return "\n".join(lines)
    except Exception as e:
        print(f"방법2 실패: {e}")

    return "❌ 순위 데이터를 가져오지 못했어요."

message = get_kbo_standings()
print(message)
requests.post(WEBHOOK_URL, json={"content": message})
print(f"전송 완료: {datetime.now()}")
