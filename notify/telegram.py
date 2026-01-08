import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

DEFAULT_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))


# =========================
# BASIC SEND / EDIT
# =========================
def send(text, chat_id=None, keyboard=None, return_message_id=False):
    payload = {
        "chat_id": chat_id or DEFAULT_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    if keyboard:
        payload["reply_markup"] = keyboard

    r = requests.post(f"{API}/sendMessage", json=payload, timeout=10)
    data = r.json()

    if return_message_id:
        return data["result"]

    return data


def edit(text, message_id, chat_id=None):
    payload = {
        "chat_id": chat_id or DEFAULT_CHAT_ID,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    requests.post(f"{API}/editMessageText", json=payload, timeout=10)


def send_to_all(text):
    from utils.users import all_users

    for uid in all_users():
        try:
            send(text, chat_id=uid)
        except Exception as e:
            print(f"❌ Telegram send error to {uid}:", e)


# =========================
# MENUS
# =========================
def main_menu(is_admin=False):
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 Market", "callback_data": "market"}],
            [{"text": "🪙 Symbols", "callback_data": "symbols"}],
            [{"text": "📰 News", "callback_data": "news"}],
        ]
    }

    if is_admin:
        keyboard["inline_keyboard"].append(
            [{"text": "⚙️ Settings", "callback_data": "settings"}]
        )

    return keyboard


def symbols_menu(state):
    """
    Меню включения / выключения торговых пар
    """
    keyboard = {"inline_keyboard": []}

    for symbol, enabled in state["symbols"].items():
        icon = "✅" if enabled else "❌"
        keyboard["inline_keyboard"].append(
            [{
                "text": f"{icon} {symbol}",
                "callback_data": f"toggle:{symbol}"
            }]
        )

    keyboard["inline_keyboard"].append(
        [{"text": "⬅️ Back", "callback_data": "back"}]
    )

    return keyboard