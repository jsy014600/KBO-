import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def get_kbo_standings():
    url = "https://m.koreabaseball.com/Kbo/TeamRank.aspx"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    # 진단용: 테이블 전체 내용 출력
    tables = soup.select("table")
    print(f"테이블 개수: {len(tables)}")
    for i, t in enumerate(tables):
        rows = t.select("tr")
        print(f"테이블{i}: {len(rows)}행")
        for row in rows[:3]:
            print(row.get_text(strip=True, separator="|"))

    return "🔍 진단 중..."

message = get_kbo_standings()
requests.post(WEBHOOK_URL, json={"content": message})
print(f"전송 완료: {datetime.now()}")
