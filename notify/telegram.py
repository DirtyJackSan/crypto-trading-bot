import os
import json
import time
import requests
from datetime import datetime, UTC

from utils.state import STATE

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 🔒 Одна сессия, без keep-alive (важно для Termux)
session = requests.Session()
session.headers.update({"Connection": "close"})


# =========================
# SEND MESSAGE
# =========================
def send(text, keyboard=None, retries=3):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)

    for attempt in range(retries):
        try:
            r = session.post(
                f"{API}/sendMessage",
                json=payload,
                timeout=15
            )
            if r.status_code == 200:
                return True
            print(f"⚠️ Telegram HTTP {r.status_code}: {r.text}")
        except Exception as e:
            print(f"❌ Telegram send error (try {attempt+1}):", e)
            time.sleep(2 * (attempt + 1))
    return False


# =========================
# MAIN MENU
# =========================
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "▶️ Торговля", "callback_data": "trade_menu"}],
            [{"text": "💱 Валюты", "callback_data": "symbols_menu"}],
            [{"text": "📊 Статус", "callback_data": "status"}],
            [{"text": "📰 Новости", "callback_data": "news_menu"}]
        ]
    }


# =========================
# SYMBOLS MENU
# =========================
def symbols_menu():
    buttons = []

    for symbol, enabled in STATE["symbols"].items():
        icon = "✅" if enabled else "❌"
        buttons.append([{
            "text": f"{icon} {symbol}",
            "callback_data": f"toggle_symbol:{symbol}"
        }])

    buttons.append([{"text": "🔙 Назад", "callback_data": "back"}])

    return {"inline_keyboard": buttons}


# =========================
# STATUS TEXT
# =========================
def status_text():
    active_symbols = [s for s, v in STATE["symbols"].items() if v]

    return (
        f"📊 <b>Статус бота</b>\n\n"
        f"▶️ Торговля: {'ВКЛ' if STATE['bot_active'] else 'ВЫКЛ'}\n"
        f"⚙️ Режим: {STATE.get('mode', 'SPOT')}\n"
        f"⚡ Плечо: x{STATE.get('leverage', 1)}\n"
        f"💱 Пары: {', '.join(active_symbols) if active_symbols else 'нет'}\n"
        f"🕒 Время: {datetime.now(UTC).strftime('%H:%M UTC')}"
    )
