import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# чат админа по умолчанию
DEFAULT_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))


# =========================
# ОТПРАВКА СООБЩЕНИЙ
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
    """
    Отправляет сообщение всем пользователям бота
    """
    from utils.users import all_users

    for uid in all_users():
        try:
            send(text, chat_id=uid)
        except Exception as e:
            print(f"❌ Telegram send error to {uid}:", e)


# =========================
# МЕНЮ
# =========================
def main_menu(is_admin=False):
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 Рынок", "callback_data": "market"}],
            [{"text": "🪙 Торговые пары", "callback_data": "symbols"}],
            [{"text": "📰 Новости", "callback_data": "news"}],
        ]
    }

    if is_admin:
        keyboard["inline_keyboard"].append(
            [{"text": "⚙️ Настройки", "callback_data": "settings"}]
        )

    return keyboard


def symbols_menu(state):
    """
    Меню включения / выключения торговых пар
    """
    keyboard = {"inline_keyboard": []}

    for symbol, enabled in state.get("symbols", {}).items():
        icon = "✅" if enabled else "❌"
        keyboard["inline_keyboard"].append(
            [{
                "text": f"{icon} {symbol}",
                "callback_data": f"toggle:{symbol}"
            }]
        )

    keyboard["inline_keyboard"].append(
        [{"text": "⬅️ Назад", "callback_data": "back"}]
    )

    return keyboard


# =========================
# СТАТУС БОТА
# =========================
def status_text(state):
    """
    Текст статуса бота (используется в handler)
    """
    lines = ["🤖 <b>Статус бота</b>\n"]

    bot_state = "🟢 ВКЛЮЧЕН" if state.get("bot_active") else "🔴 ВЫКЛЮЧЕН"
    lines.append(f"Состояние: {bot_state}\n")

    lines.append("🪙 Торговые пары:")
    for sym, enabled in state.get("symbols", {}).items():
        icon = "✅" if enabled else "❌"
        lines.append(f"{icon} {sym}")

    return "\n".join(lines)