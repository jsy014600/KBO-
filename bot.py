import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1521104717785202738/CzXHIysXBOHHTW9-wAIg4nBO41Fc7OFCuM54tDCpDbjXos49pTdjELfOwdboYk-gL9GW"

def get_kbo_standings():
    url = "https://sports.daum.net/record/kbo"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table.tbl_record tbody tr")
    lines = [f"📊 **KBO 순위** ({datetime.now().strftime('%m월 %d일')} 기준)\n"]

    medals = ["🥇", "🥈", "🥉"]
    for i, row in enumerate(rows[:10]):
        cols = row.select("td")
        if len(cols) < 3:
            continue
        rank = str(i + 1)
        team = cols[1].get_text(strip=True)
        win = cols[2].get_text(strip=True)
        lose = cols[3].get_text(strip=True)
        pct = cols[5].get_text(strip=True)
        icon = medals[i] if i < 3 else f"{rank}위"
        lines.append(f"{icon} {team}  {win}승 {lose}패  승률 {pct}")

    return "\n".join(lines)

def send_to_discord():
    try:
        message = get_kbo_standings()
        requests.post(WEBHOOK_URL, json={"content": message})
        print(f"전송 완료: {datetime.now()}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 매일 오전 9시에 전송
schedule.every().day.at("09:00").do(send_to_discord)

print("봇 시작됨! 매일 오전 9시와 오후 5시에 KBO 순위를 전송합니다.")
send_to_discord()  # 시작하자마자 한 번 바로 전송

while True:
    schedule.run_pending()
    time.sleep(60)
