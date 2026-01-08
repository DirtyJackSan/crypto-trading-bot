import requests
import os
from utils.state import STATE
from notify.telegram import send, main_menu, symbols_menu, status_text

BOT_TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def answer_callback(callback_id):
    requests.post(f"{API}/answerCallbackQuery", json={
        "callback_query_id": callback_id
    })


def process_callback(cb):
    cid = cb["id"]
    data = cb["data"]

    if data == "symbols_menu":
        send("💱 <b>Выбор валют</b>", symbols_menu())

    elif data.startswith("toggle_symbol:"):
        symbol = data.split(":")[1]
        STATE["symbols"][symbol] = not STATE["symbols"][symbol]
        send("💱 <b>Выбор валют</b>", symbols_menu())

    elif data == "status":
        send(status_text(), main_menu())

    elif data == "trade_menu":
        send(
            f"▶️ <b>Торговля</b>\n\n"
            f"Статус: {'ВКЛ' if STATE['bot_active'] else 'ВЫКЛ'}",
            {
                "inline_keyboard": [
                    [{"text": "⏯ Вкл / Выкл", "callback_data": "toggle_trade"}],
                    [{"text": "🔙 Назад", "callback_data": "back"}]
                ]
            }
        )

    elif data == "toggle_trade":
        STATE["bot_active"] = not STATE["bot_active"]
        send("📊 Главное меню", main_menu())

    elif data == "back":
        send("📊 Главное меню", main_menu())

    answer_callback(cid)
