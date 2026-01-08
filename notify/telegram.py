import os
import json
import time
import requests
from datetime import datetime, UTC

from utils.state import STATE
from utils.users import all_users

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

session = requests.Session()
session.headers.update({"Connection": "close"})


# =========================
# SEND TO ONE USER
# =========================
def send(text, keyboard=None, chat_id=None, retries=3):
    if chat_id is None:
        return False

    payload = {
        "chat_id": chat_id,
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
            print(f"❌ Telegram error (try {attempt+1}):", e)
            time.sleep(2 * (attempt + 1))

    return False


# =========================
# SEND TO ALL USERS
# =========================
def send_to_all(text, keyboard=None):
    for uid in all_users():
        send(text, keyboard=keyboard, chat_id=uid)


# =========================
# MENUS
# =========================
def main_menu(is_admin=False):
    buttons = [
        [{"text": "📊 Статус", "callback_data": "status"}],
        [{"text": "📰 Новости", "callback_data": "news_menu"}]
    ]

    if is_admin:
        buttons.insert(0, [{"text": "▶️ Торговля", "callback_data": "trade_menu"}])
        buttons.insert(1, [{"text": "💱 Валюты", "callback_data": "symbols_menu"}])

    return {"inline_keyboard": buttons}


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


def status_text():
    active = [s for s, v in STATE["symbols"].items() if v]

    return (
        f"📊 <b>Статус бота</b>\n\n"
        f"▶️ Торговля: {'ВКЛ' if STATE['bot_active'] else 'ВЫКЛ'}\n"
        f"💱 Пары: {', '.join(active) if active else 'нет'}\n"
        f"🕒 {datetime.now(UTC).strftime('%H:%M UTC')}"
    )