#pip install yfinance

import yfinance as yf
import requests
from datetime import datetime
import os
import pytz

# --- 設定區 ---
# 貼上你的 Telegram 機器人 Token 與你的 Chat ID
TG_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# 設定要查詢的股票
stocks = ['1558.TW','2330.TW', '2317.TW', 'NVDA']

# --- 抓取股價邏輯 ---
msg = f"🔔 目前時間: {datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')}\n\n"

for symbol in stocks:
    ticker = yf.Ticker(symbol)
    df = ticker.history(period='1d')
    
    if not df.empty:
        price = round(df['Close'].iloc[-1], 2)
        date = df.index[-1].strftime('%Y-%m-%d')
        msg += f"📈 {symbol}\n   價格: {price}\n   日期: {date}\n"
    else:
        msg += f"❌ {symbol} 抓取失敗\n"

# --- 發送至 Telegram ---
def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=payload)
    return response.json()

# 執行發送
result = send_telegram(msg)
if result.get("ok"):
    print("訊息已成功傳送到 Telegram！")
else:
    print(f"發送失敗，錯誤訊息：{result}")